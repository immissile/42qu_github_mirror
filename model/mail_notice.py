#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from cid import CID_INVITE_QUESTION, CID_NOTICE_QUESTION

class MailNotice(Model):
    pass

mc_mail_notice_state = McCache('MailNoticeState.%s')

@mc_mail_notice_state('{user_id}_{cid}')
def mail_notice_state(user_id, cid):
    m = MailNotice.get(user_id=user_id, cid=cid)
    if not m:
        m = MailNotice(user_id=user_id, cid=cid, state=1)
        m.save()
    return m.state

def mail_notice_set(user_id, cid, state):
    state = int(bool(state))
    MailNotice.where(user_id=user_id, cid=cid).update(state=state)
    mc_mail_notice_state.set('%s_%s' % (user_id, cid), state)
