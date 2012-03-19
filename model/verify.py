#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os import urandom
from time import time
from _db import Model, McModel, McCache, mc
from mail import mq_rendermail
from cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD, CID_VERIFY_COM_HR, CID_VERIFY_LOGIN_MAIL

from config import SITE_DOMAIN

from days import ONE_DAY

TIME_LIMIT = ONE_DAY * 7

VERIFY_TEMPLATE = {
    CID_VERIFY_MAIL: '/mail/auth/verify/mail.txt',
    CID_VERIFY_PASSWORD: '/mail/auth/verify/password.txt',
    CID_VERIFY_COM_HR:'/mail/auth/verify/com_mail.txt',
    CID_VERIFY_LOGIN_MAIL:'/mail/auth/verify/login_mail.txt',
}

class Verify(Model):
    pass

def verify_new(user_id, cid):
    v = Verify(user_id=user_id, cid=cid)
    v.create_time = time()
    value = urlsafe_b64encode(urandom(12))
    v.value = value
    v.save()
    id = v.id
    return id, value


def verify_rm(user_id, cid):
    Verify.where(user_id=user_id, cid=cid).delete()

def verify_new_one(user_id, cid):
    v = Verify.get(user_id=user_id, cid=cid)
    if not v:
        return verify_new(user_id, cid)
    return v.id, v.value

def verify_mail_new(user_id, name, mail, cid):
    id, ck = verify_new_one(user_id, cid)
    template = VERIFY_TEMPLATE[cid]
    print 'http://%s/auth/verify/login/mail/%s/%s'%(SITE_DOMAIN, id, ck)
    mq_rendermail(template, mail, name, id=id, ck=ck)

def verifyed(id, value, delete=False):
    v = Verify.get(id)
    if v:
        if delete:
            v.delete()
        if v.value == value and v.create_time + TIME_LIMIT > time():
            return v.user_id, v.cid
    return 0, 0

if __name__ == '__main__':
    #verify_mail_new(10193518,'safsadf','guohao.chu.an@gmail.com',CID_VERIFY_MAIL)
    user_id , cid = verifyed(10266, 'kvfUEfwjyOyUaHQ3')
    print user_id, cid == CID_VERIFY_COM_HR

