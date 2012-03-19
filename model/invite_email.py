#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum
from zkit.import_msn.get_friend_list import get_friend_list as msn_friend_get
#from zkit.google.ginvite import load_friend
from user_mail import user_id_by_mail
from json import dumps


CID_MSN = 1
CID_GOOGLE = 2
CID_QQ = 3

INVITE_CID2CN = {
    CID_QQ:'QQ',
    CID_GOOGLE:'Google',
    CID_MSN:'MSN',
}

GET_CID = {
        CID_MSN:msn_friend_get,
#        CID_GOOGLE:google_friend_get,
        }

class InviteEmail(Model):
    pass

class InviteMessage(Model):
    pass

def invite_message_new(user_id, email_list, txt):
    InviteMessage.raw_sql(
        'insert into invite_message (email,user_id,txt) values (%s,%s,%s)',
        dumps(email_list),
        user_id,
        txt
    )

def invite_email_new(user_id, cid, res):
    InviteEmail.raw_sql(
        'update invite_email set cid = %s where user_id =%s and cid=%s ',
        -cid, user_id, cid
    )
    for email, name in res.iteritems():
        InviteEmail.raw_sql(
'insert into invite_email (user_id, cid, email, name, email_user_id) values (%s,%s,%s,%s,%s)',
user_id, cid, email, name or email.split('@')[0], user_id_by_mail(email)
        )
    return True

def invite_user_id_by_cid(user_id, cid):
    uid = InviteEmail.raw_sql(
        'select email_user_id from invite_email where user_id = %s and cid=%s', user_id, cid
    ).fetchone()
    if uid:
        return True

def invite_invite_email_list_by_cid(user_id, cid):
    emails = InviteEmail.raw_sql('select email,name from invite_email where user_id = %s and cid=%s and email_user_id = 0', user_id, cid).fetchall()
    return emails

def invite_user_id_list_by_cid(user_id, cid):
    return InviteEmail.where('email_user_id>0').where(user_id=user_id, cid=cid).col_list(col='email_user_id')

def invite_email_list_by_cid(user_id, cid):
    return InviteEmail.where(user_id=user_id, cid=cid).col_list(col='email')

if __name__ == '__main__':
    pass

