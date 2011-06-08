#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache
from cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_PO
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

BUZZ_DIC = {
    CID_BUZZ_SYS: Po,
    CID_BUZZ_SHOW: None,
    CID_BUZZ_FOLLOW: Zsite,
    CID_BUZZ_WALL: Zsite,
    CID_BUZZ_PO: Po,
}

def buzz_new(from_id, to_id, cid, rid):
    b = Buzz(from_id=from_id, to_id=to_id, cid=cid, rid=rid, create_time=int(time()))
    b.save()
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
    follow_list = [i.from_id for i in ormiter(Follow, 'to_id=%s and from_id !=%s' % (from_id, to_id))]
    buzz_list = [i.user_id for i in ormiter(PoPos, 'po_id=%s and state=%s' % (po_id, STATE_BUZZ))]
    for user_id in set(follow_list) | set(buzz_list):
        buzz_new(from_id, user_id, CID_BUZZ_PO, po_id)

buzz_pos = Kv('buzz_pos', 0)

class BuzzEntry(object):
    def __init__(self, id, cid, rid, from_id):
        self.id = id
        self.cid = cid
        self.rid = rid
        self.from_id_list = OrderedSet([from_id])

def buzz_list(user_id, limit, offset):
    c = Buzz.raw_sql('select id, from_id, cid, rid from buzz where to_id=%s order by id desc limit %s offset %s', user_id, limit, offset)
    dic = OrderedDict()
    cls_dic = defaultdict(set)
    for id, from_id, cid, rid in c:
        key = cid, rid
        cls_dic[Zsite].add(from_id)
        if key in dic:
            dic[key].from_id_list.add(from_id)
        else:
            dic[key] = BuzzEntry(id, cid, rid, from_id)
            cls_dic[BUZZ_DIC[cid]].add(rid)
    buzz_list = dic.values()
    for cls, id_list in cls_dic.items():
        cls_dic[cls] = cls.mc_get_multi(id_list)
    for be in buzz_list:
        be.from_list = [cls_dic[Zsite][i] for i in be.from_id_list]
        be.entry = cls_dic[BUZZ_DIC[be.cid]][be.rid]
    return buzz_list

def buzz_show(user_id, limit=10):
    c = Buzz.raw_sql('select from_id, cid, rid from buzz where to_id=%s and id>%s order by id limit %s', user_id, buzz_pos.get(user_id), limit)
    return c.fetchall()[::-1]
