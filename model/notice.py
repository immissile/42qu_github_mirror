#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_INVITE_REGISTER, CID_notice_REGISTER, CID_INVITE_QUESTION, CID_notice_QUESTION
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

class Notice(McModel):
    pass

def notice_new(from_id, to_id, cid, rid=0, state=STATE_APPLY):
    n = Notice(
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
    n = notice_new(from_id, to_id, CID_INVITE_QUESTION, qid)
    return n

notice_unread_count = McNum(lambda to_id: Notice.where(to_id=to_id, state=STATE_APPLY).count(), 'NoticeUnreadCount.%s')
notice_count = McNum(lambda to_id: Notice.where(to_id=to_id).where(STATE_GTE_APPLY).count(), 'NoticeCount.%s')

mc_notice_id_list = McLimitA('NoticeIdList.%s')

@mc_notice_id_list('{to_id}')
def notice_id_list(to_id, limit, offset):
    return Notice.where(to_id=to_id).where('state>=%s' % STATE_APPLY).order_by('id desc').field_list(limit, offset)

def mc_flush(to_id):
    to_id = str(to_id)
    mc_notice_id_list.delete(to_id)
    notice_unread_count.delete(to_id)
    notice_count.delete(to_id)
