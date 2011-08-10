#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from time import time
from cid import CID_NOTICE_EVENT_NO
from state import STATE_DEL, STATE_APPLY, STATE_ACTIVE
from mail import rendermail, render_template, sendmail
from mail_notice import mail_notice_state
from user_mail import mail_by_user_id
from zkit.attrcache import attrcache

STATE_GTE_APPLY = 'state>=%s' % STATE_APPLY

mc_top_notice_id_by_user_id = McCache('TopNoticeIdByUserId.%s')


class TopNotice(McModel):
    pass


@mc_top_notice_id_by_user_id('{user_id}')
def top_notice_id_by_user_id(user_id):
    for i in TopNotice.where(user_id=user_id).where(STATE_GTE_APPLY).order_by('id desc')[:1]:
        return i.id
    return 0

def top_notice_by_user_id(user_id):
    id = top_notice_id_by_user_id(user_id)
    if id:
        return TopNotice.mc_get(id)

def top_notice_new(user_id, cid, rid, txt=''):
    o = TopNotice(user_id=user_id, cid=cid, rid=rid, txt=txt)
    o.save()
    mc_top_notice_id_by_user_id.set(user_id, o.id)
    return o

def top_notice_event_no(user_id, event_id, txt):
    return top_notice_new(user_id, CID_NOTICE_EVENT_NO, event_id, txt)

def top_notice_read(user_id, id):
    o = TopNotice.mc_get(id)
    if o and o.user_id = user_id:
        o.state = STATE_DEL
        o.save()
        mc_top_notice_id_by_user_id.delete(user_id)


if __name__ == '__main__':
    pass
