#!/usr/bin/env python
# -*- coding: utf-8 -*-
from txt2htm import RE_AT
from mq import mq_client

# id
# from_id
# to_id
# cid
# rid

BUZZ_AT_CID_PO = 1
BUZZ_AT_CID_REPLY = 2

def buzz_at_po_new(user_id, po_id, txt):
    return buzz_at_new(BUZZ_AT_CID_PO, user_id, po_id, txt)

def buzz_at_reply_new(user_id, reply_id, txt):
    return buzz_at_new(BUZZ_AT_CID_REPLY, user_id, po_id, txt)

def buzz_at_new(cid, user_id, rid, txt):
    at_id_set = set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))

    for to_id in at_id_set:
        #TODO
        #buzz_new(user_id, to_id, CID_BUZZ_WORD_AT, po_id)
        pass

    return at_id_set


mq_buzz_at_po_new = mq_client(buzz_at_po_new)


