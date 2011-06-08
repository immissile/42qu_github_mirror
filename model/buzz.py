#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_PO_REPLY
from cid import CID_USER
from zsite import Zsite
from state import STATE_ACTIVE
from follow import Follow
from po import Po
from po_pos import PoPos, STATE_BUZZ
from wall import Wall
from kv import Kv
from zweb.orm import ormiter
from zkit.orderedset import OrderedSet
from zkit.ordereddict import OrderedDict
from itertools import chain
from collections import defaultdict

class Buzz(Model):
    pass

buzz_pos = Kv('buzz_pos', 0)

buzz_count = McNum(lambda user_id: Buzz.where(to_id=user_id).count(), 'BuzzCount.%s')
buzz_unread_count = McNum(lambda user_id: Buzz.where('id>%s', buzz_pos.get(user_id)).where(to_id=user_id).count(), 'BuzzUnreadCount.%s')

BUZZ_DIC = {
    CID_BUZZ_SYS: Po,
    CID_BUZZ_SHOW: None,
    CID_BUZZ_FOLLOW: Zsite,
    CID_BUZZ_WALL: Zsite,
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

def buzz_sys_new(user_id, po_id):
    buzz_new(0, user_id, CID_BUZZ_SYS, po_id)

def buzz_sys_new_all(po_id):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, STATE_ACTIVE)):
        buzz_sys_new(i.id, po_id)

def buzz_show_new(user_id, show_id):
    buzz_new(0, user_id, CID_BUZZ_SHOW, show_id)

def buzz_show_new_all(show_id):
    for i in ormiter(Zsite, 'cid=%s and state>=%s' % (CID_USER, STATE_ACTIVE)):
        buzz_show_new(i.id, show_id)

def buzz_new_to_follow(from_id, to_id, cid):
    for i in ormiter(Follow, 'to_id=%s and from_id !=%s' % (from_id, to_id)):
        buzz_new(from_id, i.from_id, cid, to_id)

def buzz_follow_new(from_id, to_id):
    buzz_new(from_id, to_id, CID_BUZZ_FOLLOW, to_id)
    buzz_new_to_follow(from_id, to_id, CID_BUZZ_FOLLOW)

def buzz_wall_new(from_id, to_id):
    buzz_new_to_follow(from_id, to_id, CID_BUZZ_WALL)

def buzz_po_reply_new(from_id, po_id):
    followed = [i.from_id for i in ormiter(Follow, 'to_id=%s and from_id !=%s' % (from_id, to_id))]
    buzz_to = [i.user_id for i in ormiter(PoPos, 'po_id=%s and state=%s' % (po_id, STATE_BUZZ))]
    for user_id in set(followed) | set(buzz_to):
        buzz_new(from_id, user_id, CID_BUZZ_PO_REPLY, po_id)

class BuzzEntry(object):
    def __init__(self, id, cid, rid, from_id):
        self.id = id
        self.cid = cid
        self.rid = rid
        self.from_id_list = OrderedSet([from_id])

CACHE_LIMIT = 256

mc_buzz_list = McLimitM('BuzzList.%s', CACHE_LIMIT)

@mc_buzz_list('{user_id}')
def _buzz_list(user_id, limit, offset):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s order by id desc limit %s offset %s', user_id, limit, offset)
    return c.fetchall()

def buzz_pos_update(user_id, li):
    if buzz_unread_count(user_id) and li:
        id = li[0][0]
        if id > buzz_pos.get(user_id):
            buzz_pos.set(use_id, id)
            buzz_unread_count.delete(use_id)

def buzz_list(user_id, limit, offset):
    li = _buzz_list(user_id, limit, offset)
    buzz_pos_update(user_id, li[:1])
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
        cls_dic[cls] = cls.mc_get_multi(id_list)
    for be in li:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return li

def _buzz_show(user_id, limit):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s and id>%s order by id limit %s', user_id, buzz_pos.get(user_id), limit)
    return c.fetchall()

def buzz_show(user_id, limit):
    unread = buzz_unread_count(user_id)
    if unread == 0:
        return reversed(_buzz_list(user_id, limit, 0))
    elif unread <= CACHE_LIMIT:
        pos = buzz_pos.get(user_id)
        _li = reversed(_buzz_list(user_id, CACHE_LIMIT, 0))
        li = filter(lambda x: x[0] > pos, _li)[:limit]
        if len(li) < limit:
            li = _li[-limit:]
    else:
        li = _buzz_show(user_id, limit)
    buzz_pos_update(user_id, li[:1])
    return li

def buzz_show_bind(user_id, limit):
    li = []
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in buzz_show(user_id, limit):
        cls_dic[Zsite].add(from_id)
        cls_dic[BUZZ_DIC[cid]].add(rid)
        li.append(BuzzEntry(id, cid, rid, from_id))
    for cls, id_list in cls_dic.items():
        cls_dic[cls] = cls.mc_get_multi(id_list)
    for be in li:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return li
