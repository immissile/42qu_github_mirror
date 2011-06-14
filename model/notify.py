#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_INVITE_REGISTER, CID_NOTIFY_REGISTER, CID_INVITE_QUESTION, CID_NOTIFY_QUESTION
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

class Notify(McModel):
    pass

def notify_new(from_id, to_id, cid, rid=0, state=STATE_APPLY):
    n = Notify(
        from_id=from_id,
        to_id=to_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=int(time()),
    )
    n.save()
    mc_flush(to_id)
    return n

def invite_question(from_id, to_id, qid):
    n = notify_new(from_id, to_id, CID_INVITE_QUESTION, qid)
    return n

notify_unread_count = McNum(lambda to_id: Notify.where(to_id=to_id, state=STATE_APPLY).count(), 'NotifyUnreadCount.%s')
notify_count = McNum(lambda to_id: Notify.where(to_id=to_id).where(STATE_GTE_APPLY).count(), 'NotifyCount.%s')

mc_notify_id_list = McLimitA('NotifyIdList.%s')

@mc_notify_id_list('{to_id}')
def notify_id_list(to_id, limit, offset):
    return Notify.where(to_id=to_id).where('state>=%s' % STATE_APPLY).field_list(limit, offset)

def mc_flush(to_id):
    to_id = str(to_id)
    mc_notify_id_list.delete(to_id)
    notify_unread_count.delete(to_id)
    notify_count.delete(to_id)
