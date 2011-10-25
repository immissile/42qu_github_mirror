#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
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

GET_CID ={
        CID_MSN:msn_friend_get,
#        CID_GOOGLE:google_friend_get,
        }

class InviteEmail(Model):
    pass

class InviteMessage(Model):
    pass

def new_invite_message(uid,email_list,txt):
    InviteMessage.raw_sql('insert into invite_message (email,uid,txt) values (%s,%s,%s)',dumps(email_list),uid,txt)

def new_invite_email(usr_id,cid_email,cid,res):
    InviteEmail.raw_sql('update invite_email set cid = %s where usr_id =%s and cid=%s ',-cid,usr_id,cid)
    for email,name in res.items():
        InviteEmail.raw_sql('insert into invite_email (usr_id,cid,cid_email,email,name,email_uid) values(%s,%s,%s,%s,%s,%s)',usr_id,cid,cid_email,email,name,user_id_by_mail(email))
    return True

def get_invite_uid_by_cid(usr_id,cid):
    uid = InviteEmail.raw_sql('select email_uid from invite_email where usr_id = %s and cid=%s',usr_id,cid).fetchone()
    if uid:
        return True
def get_invite_email_list_by_cid(usr_id,cid):
    emails = InviteEmail.raw_sql('select email,name from invite_email where usr_id = %s and cid=%s and email_uid = 0',usr_id,cid).fetchall()
    return emails

def get_invite_uid_list_by_cid(usr_id,cid):
    uid_list = InviteEmail.raw_sql('select email_uid from invite_email where usr_id = %s and cid = %s',usr_id,cid).fetchall()
    full_uid = []
    for uid in uid_list:
        if uid[0]:
            full_uid.append(uid[0])
    return full_uid

def get_email_by_cid(usr_id,cid):
    return [i.email for i in InviteEmail.where(usr_id=usr_id).where(cid=cid)]

if __name__ == "__main__":
    print msn_friend_get('wsyupeng@hotmail.com','yu6171446')
