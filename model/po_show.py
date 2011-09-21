#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache
from feed import feed_rt, feed_rt_rm
from po import Po, po_new, po_word_new, po_note_new, po_rm, CID_QUESTION
from rank import Rank, rank_po_id_list, rank_new, rank_rm, rank_po_id_count, rank_id_by_po_id_to_id, _rank_mv
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from zsite import Zsite

ORDER = ('id', 'hot', 'confidence')

def po_show_new(po, cid=0):
    r = rank_new(po, 0, cid)
    feed_rt(0, po.id)

def po_show_rm(po_id):
    feed_rt_rm(0, po_id)
    rank_rm(po_id, 0)

def po_show_list(cid, order, limit, offset):
    ids = rank_po_id_list(0, cid, order, limit, offset)
    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li

def po_show_count(cid=0):
    return rank_po_id_count(0, cid)

def po_is_show(po):
    return bool(rank_id_by_po_id_to_id(po.id, 0))

def po_show_set(po, cid):
    po_id = po.id
    id = rank_id_by_po_id_to_id(po_id, 0)
    r = Rank.mc_get(id)
    if r:
        if cid:
            _rank_mv(r, cid)
        else:
            po_show_rm(po_id)
    else:
        po_show_new(po, cid)

#Po.is_show = property(po_is_show)

if __name__ == '__main__':
    for i in po_show_list(0, 'id', 25, 0):
        print i.name_
