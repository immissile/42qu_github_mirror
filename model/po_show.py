#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache
from feed import feed_rt, feed_rt_rm, feed_rt_list, feed_rt_count, feed_rt_id
from po import Po, po_new, po_word_new, po_note_new, po_rm, CID_QUESTION
from state import STATE_RM, STATE_SECRET, STATE_ACTIVE
from zsite import Zsite
#from rank import Rank, rank_po_id_list, rank_new, rank_rm, rank_po_id_count, rank_id_by_po_id_to_id, _rank_mv
from _db import cursor_by_table
from cid import CID_REC

cursor = cursor_by_table('feed')
def po_show_new(po):
    feed_rt(0, po.id)

def po_show_rm(po_id):
    feed_rt_rm(0, po_id)
    Po.where(user_id=0, rid=po.id, cid=CID_REC, state=STATE_ACTIVE).delete()

def po_show_list(limit, offset):
    ids = feed_rt_list(0, limit, offset)
    li = Po.mc_get_list(ids)
    li = Po.mc_get_list(i.rid for i in li)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li

def po_show_count():
    return feed_rt_count(0)

def po_is_show(po):
    r = Po.get(user_id=0, rid=po.id, cid=CID_REC, state=STATE_ACTIVE)
    if r:
        return r.id


if __name__ == '__main__':
    po = Po.mc_get(10218451)
#    po_show_rm(po.id)
#    print po_is_show(po)

