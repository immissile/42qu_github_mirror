#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from txt2htm import RE_AT
from cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_WALL_REPLY, CID_BUZZ_PO_REPLY, CID_BUZZ_ANSWER, CID_BUZZ_JOIN, CID_BUZZ_EVENT_JOIN_APPLY, CID_BUZZ_EVENT_FEEDBACK_JOINER, CID_BUZZ_EVENT_FEEDBACK_OWNER, CID_USER, CID_BUZZ_SITE_NEW , CID_BUZZ_SITE_FAV, CID_BUZZ_WORD

from zsite import Zsite, ZSITE_STATE_ACTIVE
from follow import Follow
from po import Po
from po_pos import PoPos, STATE_BUZZ
from state import STATE_BUZZ_ACTIVE, STATE_BUZZ_RM
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

def buzz_set_read(user_id, buzz_id):
    buzz = Buzz.get(buzz_id)
    if buzz:
        buzz.state = STATE_BUZZ_RM
        buzz.save()
    mc_flush(user_id)


def clear_buzz_by_po_id(user_id,po_id):
    po = Po.mc_get(po_id)
    if po:
        reply_id_list = po.reply_id_list()
        for reply in reply_id_list:
            buzz_list = Buzz.where(to_id = user_id).where(cid=CID_BUZZ_PO_REPLY).where(rid = reply)
            if buzz_list:
                for buzz in buzz_list:
                    buzz_set_read(user_id,buzz.id)

def buzz_unread_count(user_id):
    #count = buzz_unread.get(user_id)
    count = Buzz.where("state >%s"%STATE_BUZZ_RM).where(to_id=user_id).count()

    #if count is None or count is False:
    #    count = Buzz.where('id>%s', buzz_pos.get(user_id)).where(to_id=user_id).count()
    #    #buzz_unread.set(
    #    #    user_id, count
    #    #)
    return count

BUZZ_DIC = {
    CID_BUZZ_SYS: BuzzSys,
    CID_BUZZ_SHOW: Zsite,
    CID_BUZZ_FOLLOW: Zsite,
    CID_BUZZ_WALL: Wall,
    CID_BUZZ_WALL_REPLY: Wall,
    CID_BUZZ_PO_REPLY: Reply,
    CID_BUZZ_ANSWER: Po,
    CID_BUZZ_WORD: Po,
    CID_BUZZ_JOIN: Po,
    CID_BUZZ_EVENT_JOIN_APPLY: Po,
    CID_BUZZ_EVENT_FEEDBACK_OWNER: Po,
    CID_BUZZ_EVENT_FEEDBACK_JOINER: Po,
    CID_BUZZ_SITE_NEW : Zsite,
    CID_BUZZ_SITE_FAV : Zsite,
}

def mc_flush(user_id):
    buzz_count.delete(user_id)
    mc_buzz_list.delete(user_id)
    #buzz_unread_count.delete(user_id)

def buzz_new(from_id, to_id, cid, rid):
    b = Buzz(from_id=from_id, to_id=to_id, cid=cid, rid=rid, create_time=int(time()), state=STATE_BUZZ_ACTIVE)
    b.save()
    mc_flush(to_id)
    buzz_unread_update(to_id)
    return b

def buzz_sys_new(user_id, rid):
    buzz_new(0, user_id, CID_BUZZ_SYS, rid)

def buzz_sys_new_all(rid):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, ZSITE_STATE_ACTIVE)):
        buzz_sys_new(i.id, rid)

#mq_buzz_sys_new_all = mq_client(buzz_sys_new_all)

def buzz_show_new(user_id, zsite_id):
    buzz_new(0, user_id, CID_BUZZ_SHOW, zsite_id)

def buzz_show_new_all(zsite_id):
    for i in ormiter(BuzzUnread, 'value < 10'):
        buzz_show_new(i.id, zsite_id)
#        print i.id, zsite_id

def buzz_follow_new(from_id, to_id):
    if not Buzz.where(from_id=from_id, to_id=to_id, cid=CID_BUZZ_FOLLOW, rid=to_id).count():
        buzz_new(from_id, to_id, CID_BUZZ_FOLLOW, to_id)
        for i in ormiter(Follow, 'to_id=%s and from_id!=%s' % (from_id, to_id)):
            buzz_new(from_id, i.from_id, CID_BUZZ_FOLLOW, to_id)

mq_buzz_follow_new = mq_client(buzz_follow_new)

def buzz_wall_new(from_id, to_id, wall_id):
    for i in ormiter(Follow, 'to_id=%s and from_id!=%s' % (from_id, to_id)):
        buzz_new(from_id, i.from_id, CID_BUZZ_WALL, wall_id)

mq_buzz_wall_new = mq_client(buzz_wall_new)

def buzz_wall_reply_new(from_id, to_id, wall_id):
    buzz_new(from_id, to_id, CID_BUZZ_WALL_REPLY, wall_id)


def buzz_word_new(user_id, po_id, txt ):
    ated = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))
    for to_id in ated:
        buzz_new(user_id, to_id, CID_BUZZ_WORD, po_id)

mq_buzz_word_new = mq_client(buzz_word_new)

def buzz_po_reply_new(from_id, reply_id, po_id, po_user_id):
    from txt import txt_get
    from po_pos import po_pos_state, STATE_MUTE
    txt = txt_get(reply_id)
    ated = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

    followed = set([i.from_id for i in ormiter(Follow, 'to_id=%s' % from_id)])
    buzz_to = set([i.user_id for i in ormiter(PoPos, 'po_id=%s and state=%s' % (po_id, STATE_BUZZ))])
    excepted = set([from_id, po_user_id])

    if from_id != po_user_id:
        buzz_new(from_id, po_user_id, CID_BUZZ_PO_REPLY, reply_id)

    for user_id in ((ated | followed | buzz_to) - excepted):
        buzz_new(from_id, user_id, CID_BUZZ_PO_REPLY, reply_id)
        po_pos_state(user_id, po_id, STATE_MUTE)

mq_buzz_po_reply_new = mq_client(buzz_po_reply_new)

def buzz_po_reply_rm(reply_id):
    for i in ormiter(Buzz, 'cid=%s and rid=%s' % (CID_BUZZ_PO_REPLY, reply_id)):
        to_id = i.to_id
        i.delete()
        mc_flush(to_id)
        buzz_unread_update(to_id)

mq_buzz_po_reply_rm = mq_client(buzz_po_reply_rm)

def buzz_po_rm(po_id):
    to_id_list = set()
    po = Po.mc_get(po_id)
    to_id_list = set()
    for reply_id in po.reply_id_list():
        for i in ormiter(Buzz, 'cid=%s and rid=%s' % (CID_BUZZ_PO_REPLY, reply_id)):
            to_id_list.add(i.to_id)
            i.delete()
    for to_id in to_id_list:
        mc_flush(to_id)
        buzz_unread_update(to_id)

mq_buzz_po_rm = mq_client(buzz_po_rm)

def buzz_answer_new(from_id, po_id):
    from po_question import po_user_id_list
    for user_id in po_user_id_list(po_id):
        if user_id != from_id:
            buzz_new(from_id, user_id, CID_BUZZ_ANSWER, po_id)

mq_buzz_answer_new = mq_client(buzz_answer_new)


class BuzzEntry(object):
    def __init__(self, id, cid, rid, from_id):
        self.id = id
        self.cid = cid
        self.rid = rid
        self.from_id_list = OrderedSet(from_id)

def buzz_pos_update(user_id, li):
    if li:
        id = li[0][0]
        if id > buzz_pos.get(user_id):
            buzz_pos.set(user_id, id)
            buzz_unread_update(user_id)

CACHE_LIMIT = 256

mc_buzz_list = McLimitM('BuzzList.%s', CACHE_LIMIT)

#@mc_buzz_list('{user_id}')
def _buzz_list(user_id, limit, offset, state=STATE_BUZZ_ACTIVE):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s and state >= %s order by id desc limit %s offset %s', user_id, state, limit, offset)
    return c.fetchall()

def buzz_list(user_id, limit, offset,state = STATE_BUZZ_ACTIVE):
    li = _buzz_list(user_id, limit, offset,state = state)
    if not li:
        return []
    #buzz_pos_update(user_id, li)
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in li:
        key = cid, rid
        cls_dic[Zsite].add(from_id)
        if key in dic:
            dic[key].from_id_list.add(from_id)
        else:
            dic[key] = BuzzEntry(id, cid, rid, [from_id])
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
        if i.cid in (CID_BUZZ_SHOW, CID_BUZZ_FOLLOW):
            id_list.append(i.rid)
    c_dict = career_dict(id_list)
    for i in li:
        if i.cid in (CID_BUZZ_SHOW, CID_BUZZ_FOLLOW):
            i.entry.career = c_dict[i.rid]
    return li

def _buzz_show(user_id, limit, unread=None):
    #if unread is None:
    #    unread = buzz_unread_count(user_id)
    #if not unread:
    #    return []
    #limit = min(unread, limit)
    offset = max(unread - limit, 0)
    li = _buzz_list(user_id, limit, offset)
    return li

def _buzz_list_by_cid(user_id, limit, cid, state=STATE_BUZZ_ACTIVE):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s and state >= %s and cid=%s order by id desc limit %s ', user_id, state,cid, limit)
    return c.fetchall()

def buzz_show_by_cid(user_id,limit,cid,state=STATE_BUZZ_ACTIVE):
    _li = _buzz_list_by_cid(user_id, limit, cid,state = state)
    if not _li:
        return []
    li = []
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    buzz_dic = defaultdict(list)
    for id, from_id, cid, rid in _li:
        cls_dic[Zsite].add(from_id)
        cls_dic[BUZZ_DIC[cid]].add(rid)
        li.append(BuzzEntry(id, cid, rid, [from_id]))
        if id not in buzz_dic:
            buzz_dic[id] =[id, cid,rid,[from_id]]
        else:
            buzz_dic[id][3].append(from_id)
            buzz_dic[id][3]= list(set(buzz_dic[id][3]))

    for cls, id_list in cls_dic.items():
        cls_dic[cls] = cls.mc_get_dict(id_list)

    for be in li:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return buzz_career_bind(li)

def buzz_show(user_id, limit, unread=None):
    _li = _buzz_show(user_id, limit, unread)
    if not _li:
        return []
    #buzz_pos_update(user_id, _li)
    li = []
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in _li:
        cls_dic[Zsite].add(from_id)
        cls_dic[BUZZ_DIC[cid]].add(rid)
        li.append(BuzzEntry(id, cid, rid, [from_id]))
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
            buzz_new(user_id, to_id, CID_BUZZ_JOIN, event_id)

mq_buzz_event_join_new = mq_client(buzz_event_join_new)
#mq_buzz_event_join_new = buzz_event_join_new


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
    #listB = _buzz_list(10031395,1000,0)
    #for id, from_id, cid, rid in listB:
    #    buzz_set_read(10031395,id)
#    from model.zsite import Zsite
#    from model.cid import CID_USER
#    print buzz_unread_update(10000000)
#    print buzz_unread_count(10000000)
#    print buzz_show(10000000, 3)
    #import time
    #for i in range(100):
    #    print Buzz.where(cid=CID_BUZZ_FOLLOW).delete()
    #    time.sleep(1)
    #    print Buzz.where(cid=CID_BUZZ_FOLLOW).count()
