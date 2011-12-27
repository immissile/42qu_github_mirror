#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import cursor_by_table, McModel, McLimitA, McCache, McCacheA
from txt2htm import RE_AT
from txt import txt_bind, txt_get, txt_new
from mq import mq_client
from buzz_at import buzz_at_new
from kv import Kv

# buzz_at
# id
# from_id
# to_id
# po_id
# reply_id
# state

# buzz_at_pos
# id
# value

BUZZ_AT_SHOW    = 30
BUZZ_AT_HIDE    = 20
BUZZ_AT_RMED    =  0

buzz_at_pos = Kv("buzz_at_pos", int)

class BuzzAt(Model):
    pass

def at_id_set_by_txt(txt):
    return set(filter(bool, [id_by_url(i[2]) for i in RE_AT.findall(txt)]))


def buzz_at_new(from_id, txt, po_id, reply_id=0):
    at_id_set = at_id_set_by_txt(txt)

    for to_id in at_id_set:
        buzz_at = BuzzAt(from_id=from_id, to_id=to_id, reply_id=reply_id, po_id=po_id,state=BUZZ_AT_SHOW)
        buzz_at.save()

    return at_id_set

mq_buzz_at_new = mq_client(buzz_at_new)


def buzz_at_reply_rm(reply_id):
    from model.reply import Reply
    txt = txt_get(reply_id)
    if not txt:
        return
    at_id_set = at_id_set_by_txt(txt)
    for to_id in at_id_set:
        BuzzAt.where(to_id=to_id, reply_id=reply_id).update(state=BUZZ_AT_RMED)


def buzz_at_by_user_id_for_show(user_id):
    begin_id = buzz_at_pos.get(user_id)
    buzz_at_list = reversed(BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).where("id>%s",begin_id).order_by("id")[:5])
    result = []
    for i in buzz_at_list:
        result.append( (i.from_id, i.po_id, i.reply_id) )
    return result



def buzz_at_list(user_id, limit, offset):
    BuzzAt.where(to_id=user_id, state=BUZZ_AT_SHOW).order_by("id desc")[offset:offset+limit]
    pass

