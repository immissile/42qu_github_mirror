#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McLimitM, McNum
from cid import CID_BUZZ_SYS, CID_BUZZ_FOLLOW, CID_BUZZ_EVENT_JOIN,  CID_BUZZ_EVENT_FEEDBACK_JOINER, CID_BUZZ_EVENT_FEEDBACK_OWNER, CID_USER, CID_BUZZ_SITE_NEW , CID_BUZZ_SITE_FAV, CID_BUZZ_PO_FAV
from zsite import Zsite, ZSITE_STATE_ACTIVE
from follow import Follow
from po import Po
from po_pos import PoPos, STATE_BUZZ
from buzz_sys import BuzzSys
from wall import Wall
from kv import Kv
from mq import mq_client
from career import career_dict
from reply import Reply
from zweb.orm import ormiter
from zkit.orderedset import OrderedSet
from zkit.ordereddict import OrderedDict
from zsite_url import id_by_url
from collections import defaultdict

class Buzz(Model):
    pass

class BuzzUnread(Model):
    pass

buzz_pos = Kv('buzz_pos', 0)
buzz_unread = Kv('buzz_unread', None)

buzz_count = McNum(lambda user_id: Buzz.where(to_id=user_id).count(), 'BuzzCount.%s')
#buzz_unread_count = McNum(lambda user_id: Buzz.where('id>%s', buzz_pos.get(user_id)).where(to_id=user_id).count(), 'BuzzUnreadCount.%s')


def buzz_unread_count(user_id):
    count = buzz_unread.get(user_id)
    if count is None or count is False:
        count = Buzz.where('id>%s', buzz_pos.get(user_id)).where(to_id=user_id).count()
        buzz_unread.set(
            user_id, count
        )
    return count

BUZZ_DIC = {
    CID_BUZZ_SYS: BuzzSys,
    CID_BUZZ_FOLLOW: Zsite,
    CID_BUZZ_EVENT_JOIN: Po,
    CID_BUZZ_EVENT_FEEDBACK_OWNER: Po,
    CID_BUZZ_EVENT_FEEDBACK_JOINER: Po,
    CID_BUZZ_PO_FAV: Po,
    CID_BUZZ_SITE_NEW : Zsite,
    CID_BUZZ_SITE_FAV : Zsite,
}

def mc_flush(user_id):
    buzz_count.delete(user_id)
    mc_buzz_list.delete(user_id)
    #buzz_unread_count.delete(user_id)

def buzz_new(from_id, to_id, cid, rid):
    b = Buzz(from_id=from_id, to_id=to_id, cid=cid, rid=rid, create_time=int(time()))
    b.save()
    mc_flush(to_id)
    buzz_unread_update(to_id)
    return b

def buzz_po_fav_new(from_id, po_id):
    for i in ormiter(Follow, 'to_id=%s and from_id!=%s' % (from_id, from_id)):
        buzz_new(from_id, i.from_id, CID_BUZZ_PO_FAV, po_id)
    
mq_buzz_po_fav_new = mq_client(buzz_po_fav_new)

def buzz_sys_new(user_id, rid):
    buzz_new(0, user_id, CID_BUZZ_SYS, rid)

def buzz_sys_new_all(rid):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, ZSITE_STATE_ACTIVE)):
        buzz_sys_new(i.id, rid)

#mq_buzz_sys_new_all = mq_client(buzz_sys_new_all)



def buzz_follow_new(from_id, to_id):
    if not Buzz.where(from_id=from_id, to_id=to_id, cid=CID_BUZZ_FOLLOW, rid=to_id).count():
        buzz_new(from_id, to_id, CID_BUZZ_FOLLOW, to_id)
        for i in ormiter(Follow, 'to_id=%s and from_id!=%s' % (from_id, to_id)):
            buzz_new(from_id, i.from_id, CID_BUZZ_FOLLOW, to_id)

mq_buzz_follow_new = mq_client(buzz_follow_new)




class BuzzEntry(object):
    def __init__(self, id, cid, rid, from_id):
        self.id = id
        self.cid = cid
        self.rid = rid
        self.from_id_list = OrderedSet([from_id])

def buzz_pos_update(user_id, li):
    if li:
        id = li[0][0]
        if id > buzz_pos.get(user_id):
            buzz_pos.set(user_id, id)
            buzz_unread_update(user_id)

CACHE_LIMIT = 256

mc_buzz_list = McLimitM('BuzzList.%s', CACHE_LIMIT)

@mc_buzz_list('{user_id}')
def _buzz_list(user_id, limit, offset):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s order by id desc limit %s offset %s', user_id, limit, offset)
    return c.fetchall()

def buzz_list(user_id, limit, offset):
    li = _buzz_list(user_id, limit, offset)
    if not li:
        return []
    buzz_pos_update(user_id, li)
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in li:
        key = cid, rid
        cls_dic[Zsite].add(from_id)
        if key in dic:
            dic[key].from_id_list.add(from_id)
        else:
            dic[key] = BuzzEntry(id, cid, rid, from_id)
            cls_dic[BUZZ_DIC[cid]].add(rid)
    li = dic.values()
    for cls, id_list in cls_dic.items():
        cls_dic[cls] = cls.mc_get_dict(id_list)
    for be in li:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return buzz_career_bind(li)

def buzz_career_bind(li):
    id_list = []
    for i in li:
        if i.cid == CID_BUZZ_FOLLOW:
            id_list.append(i.rid)
    c_dict = career_dict(id_list)
    for i in li:
        if i.cid == CID_BUZZ_FOLLOW:
            i.entry.career = c_dict[i.rid]
    return li

def _buzz_show(user_id, limit, unread=None):
    if unread is None:
        unread = buzz_unread_count(user_id)
    if not unread:
        return []
    limit = min(unread, limit)
    offset = max(unread - limit, 0)
    li = _buzz_list(user_id, limit, offset)
    return li

def buzz_show(user_id, limit, unread=None):
    _li = _buzz_show(user_id, limit, unread)
    if not _li:
        return []
    buzz_pos_update(user_id, _li)
    li = []
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in _li:
        cls_dic[Zsite].add(from_id)
        cls_dic[BUZZ_DIC[cid]].add(rid)
        li.append(BuzzEntry(id, cid, rid, from_id))
    for cls, id_list in cls_dic.items():
        cls_dic[cls] = cls.mc_get_dict(id_list)
    for be in li:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return buzz_career_bind(li)

#def buzz_unread_incr(user_id):
#    unread = buzz_unread_count(user_id)
#    buzz_unread.set(user_id, unread + 1)


def buzz_unread_update(user_id):
    buzz_unread.set(user_id, None)

def buzz_event_join_new(user_id, event_id, zsite_id):
    followed = [i.from_id for i in ormiter(Follow, 'to_id=%s' % user_id)]
    for to_id in followed:
        if to_id != zsite_id:
            buzz_new(user_id, to_id, CID_BUZZ_EVENT_JOIN, event_id)

mq_buzz_event_join_new = mq_client(buzz_event_join_new)


def buzz_event_join_apply_new(user_id, zsite_id, event_id):
    buzz_new(user_id, zsite_id, CID_BUZZ_EVENT_JOIN_APPLY, event_id)


# 张沈鹏 评论了 <a>去看电影</a> , 点此浏览
# 只显示给发起人
def buzz_event_feedback_new(user_id, event_id, event_user_id):
    buzz_new(user_id, event_user_id, CID_BUZZ_EVENT_FEEDBACK_JOINER, event_id)


# 张沈鹏 写了 <a>去看电影</a> 的活动总结 , 点此浏览
# 显示给所有人
def buzz_event_feedback_owner_new(user_id, event_id):
    from event import event_joiner_user_id_list
    to_id_list = event_joiner_user_id_list(event_id)
    for to_id in to_id_list:
        buzz_new(user_id, to_id, CID_BUZZ_EVENT_FEEDBACK_OWNER, event_id)

mq_buzz_event_feedback_owner_new = mq_client(buzz_event_feedback_owner_new)


def buzz_site_fav(user_id, site_id):
    followed = Follow.where('to_id=%s', user_id).col_list(col='from_id')
    for to_id in followed:
        buzz_new(user_id, to_id, CID_BUZZ_SITE_FAV, site_id)

mq_buzz_site_fav = mq_client(buzz_site_fav)

def buzz_site_new(user_id, site_id):
    followed = Follow.where('to_id=%s', user_id).col_list(col='from_id')
    for to_id in followed:
        buzz_new(user_id, to_id, CID_BUZZ_SITE_NEW , site_id)

mq_buzz_site_new = mq_client(buzz_site_new)



if __name__ == '__main__':
    pass
#    from model.zsite import Zsite
#    from model.cid import CID_USER
#    print buzz_unread_update(10000000)
#    print buzz_unread_count(10000000)
#    print buzz_show(10000000, 3)
    import time
    for i in Buzz.where(cid=216)[:3]:
        print i
