#!/usr/bin/env python
# -*- coding: utf-8 -*-
from po import Po, po_new, po_word_new, po_note_new, po_rm, CID_QUESTION
from rank import rank_po_id_list, rank_new
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE

def po_show_new(po, cid):
    from feed import feed_rt
    rank_new(po, 0, cid)
    feed_rt(0, po.id)

def po_show_list(cid, order, limit, offset):
    ids = rank_po_id_list(0, cid, order, limit, offset)
    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')
    return li

def po_show_hot(cid, limit, offset):
    return po_show_list(cid, 'hot', limit, offset)

def po_show_confidence(cid, limit, offset):
    return po_show_list(cid, 'confidence', limit, offset)
