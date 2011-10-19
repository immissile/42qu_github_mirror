#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import Model, McModel, McCache, McLimitM, McNum
from zkit.import_msn.get_friend_list import get_friend_list as msn_friend_get
#from zkit.google.ginvite import load_friend
from user_mail import user_id_by_mail
CID_MSN = 1
CID_GOOGLE = 2

GET_CID ={
        CID_MSN:msn_friend_get,
#        CID_GOOGLE:google_friend_get,
        }

class InviteEmail(Model):
    pass

def new_invite_email(usr_id,cid_email,cid,res):
    InviteEmail.raw_sql('update invite_email set cid = %s where usr_id =%s and cid=%s ',-cid,usr_id,cid)
    for email,name in res.items():
        InviteEmail.raw_sql('insert into invite_email (usr_id,cid,cid_email,email,name,email_uid) values(%s,%s,%s,%s,%s,%s)',usr_id,cid,cid_email,email,name,user_id_by_mail(email))
    return True

def get_email_by_cid(usr_id,cid):
    return [i.email for i in InviteEmail.where(usr_id=usr_id).where(cid=cid)]

if __name__ == "__main__":
    print msn_friend_get('wsyupeng@hotmail.com','yu6171446')
