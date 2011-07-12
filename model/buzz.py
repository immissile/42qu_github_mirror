#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_WALL_REPLY, CID_BUZZ_PO_REPLY
from cid import CID_USER
from zsite import Zsite, ZSITE_STATE_APPLY
from follow import Follow
from po import Po
from po_pos import PoPos, STATE_BUZZ
from buzz_sys import BuzzSys
from wall import Wall
from kv import Kv
from mq import mq_client
from career import career_dict
from zweb.orm import ormiter
from zkit.orderedset import OrderedSet
from zkit.ordereddict import OrderedDict
from collections import defaultdict

class Buzz(Model):
    pass

buzz_pos = Kv('buzz_pos', 0)

buzz_count = McNum(lambda user_id: Buzz.where(to_id=user_id).count(), 'BuzzCount.%s')
buzz_unread_count = McNum(lambda user_id: Buzz.where('id>%s', buzz_pos.get(user_id)).where(to_id=user_id).count(), 'BuzzUnreadCount.%s')

BUZZ_DIC = {
    CID_BUZZ_SYS: BuzzSys,
    CID_BUZZ_SHOW: Zsite,
    CID_BUZZ_FOLLOW: Zsite,
    CID_BUZZ_WALL: Wall,
    CID_BUZZ_WALL_REPLY: Wall,
    CID_BUZZ_PO_REPLY: Po,
}

def mc_flush(user_id):
    buzz_count.delete(user_id)
    buzz_unread_count.delete(user_id)
    mc_buzz_list.delete(user_id)

def buzz_new(from_id, to_id, cid, rid):
    b = Buzz(from_id=from_id, to_id=to_id, cid=cid, rid=rid, create_time=int(time()))
    b.save()
    mc_flush(to_id)
    return b

def buzz_sys_new(user_id, rid):
    buzz_new(0, user_id, CID_BUZZ_SYS, rid)

def buzz_sys_new_all(rid):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, ZSITE_STATE_APPLY)):
        buzz_sys_new(i.id, rid)

mq_buzz_sys_new_all = mq_client(buzz_sys_new_all)

def buzz_show_new(user_id, zsite_id):
    buzz_new(0, user_id, CID_BUZZ_SHOW, zsite_id)

def buzz_show_new_all(zsite_id):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, ZSITE_STATE_APPLY)):
        buzz_show_new(i.id, zsite_id)

def buzz_follow_new(from_id, to_id):
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

def buzz_po_reply_new(from_id, po_id):
    followed = [i.from_id for i in ormiter(Follow, 'to_id=%s' % from_id)]
    buzz_to = [i.user_id for i in ormiter(PoPos, 'po_id=%s and state=%s' % (po_id, STATE_BUZZ))]
    for user_id in (set(followed) | set(buzz_to)) - set([from_id]):
        buzz_new(from_id, user_id, CID_BUZZ_PO_REPLY, po_id)

mq_buzz_po_reply_new = mq_client(buzz_po_reply_new)

class BuzzEntry(object):
    def __init__(self, id, cid, rid, from_id):
        self.id = id
        self.cid = cid
        self.rid = rid
        self.from_id_list = OrderedSet([from_id])

def buzz_pos_update(user_id, li):
    if buzz_unread_count(user_id) and li:
        id = li[0][0]
        if id > buzz_pos.get(user_id):
            buzz_pos.set(user_id, id)
            buzz_unread_count.delete(user_id)

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
        if i.cid == CID_BUZZ_SHOW:
            id_list.append(i.rid)
    c_dict = career_dict(id_list)
    for i in li:
        if i.cid == CID_BUZZ_SHOW:
            i.entry.career = c_dict[i.rid]
    return li

def _buzz_show(user_id, limit):
    unread = buzz_unread_count(user_id)
    if not unread:
        return []
    limit = min(unread, limit)
    offset = max(unread - limit, 0)
    li = _buzz_list(user_id, limit, offset)
    return li

def buzz_show(user_id, limit):
    _li = _buzz_show(user_id, limit)
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

if __name__ == '__main__':
    #buzz_show_new_all(10024800)
    pass
#    for i in buzz_list(10000000, 100, 0):
#        pass
#        print i.id
#        print i.cid
#
  #  from model.zsite import Zsite
  #  c = Buzz.raw_sql("select distinct rid from buzz where cid=%s",CID_BUZZ_SHOW)
  #  for i, in c:
  #      zsite = Zsite.mc_get(i)
  #      if not zsite:
    Buzz.raw_sql("delete from buzz where cid=%s and rid=%s", CID_BUZZ_SHOW, 10000000)

    #Buzz.where(rid=10003473,cid=CID_BUZZ_SHOW).delete()
