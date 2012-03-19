#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McNum
from cid import CID_MAIL_DAY, CID_MAIL_MONTH, CID_MAIL_YEAR, CID_BUZZ_FOLLOW, CID_MAIL_WEEK
from model.zsite import Zsite, CID_USER
from user_mail import mail_by_user_id
from zweb.orm import ormiter

CID_MAIL_NOTICE_ALL = (
    CID_BUZZ_FOLLOW,
#    CID_INVITE_QUESTION,
    CID_MAIL_DAY,
    CID_MAIL_MONTH,
    CID_MAIL_YEAR,
    CID_MAIL_WEEK,
)

class MailNotice(Model):
    pass

mc_mail_notice_state = McCache('MailNoticeState.%s')

@mc_mail_notice_state('{user_id}_{cid}')
def mail_notice_state(user_id, cid):
    m = MailNotice.get(user_id=user_id, cid=cid)
    if not m:
        MailNotice.raw_sql('insert into mail_notice (user_id, cid, state) values (%s, %s, 1) on duplicate key update state=state', user_id, cid)
        m = MailNotice.get(user_id=user_id, cid=cid)
    return m.state

def mail_notice_all(user_id):
    return [(cid, mail_notice_state(user_id, cid)) for cid in CID_MAIL_NOTICE_ALL]

def mail_notice_set(user_id, cid, state):
    state = int(bool(state))
    if state != mail_notice_state(user_id, cid):
        MailNotice.where(user_id=user_id, cid=cid).update(state=state)
        mc_mail_notice_state.set('%s_%s' % (user_id, cid), state)

def mail_notice_iter(cid):
    for i in ormiter(Zsite, 'cid=%s'%CID_USER):
        if mail_notice_state(i.id , cid):
            mail = mail_by_user_id(i.id)
            yield mail, i.name


if __name__ == '__main__':
    #MailNotice.where(cid=CID_MAIL_WEEK).delete()
    #MailNotice.raw_sql('insert into mail_notice (user_id, cid, state) select user_id, %s, state from mail_notice where cid=%s', CID_MAIL_WEEK, CID_MAIL_MONTH)
    pass
