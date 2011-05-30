#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os import urandom
from time import time
from _db import Model, McModel, McCache, mc, cursor_by_table
from mail import mq_rendermail
from cid import CID_VERIFY_MAIL

TIME_LIMIT = 3600 * 24 * 7

VERIFY_TEMPLATE = {
    CID_VERIFY_MAIL: '/mail/auth/register.txt',
}

class UserVerify(Model):
    pass


def _user_verify_new(user_id, cid):
    v = UserVerify(user_id=user_id, cid=cid)
    v.create_time = time()
    value = urlsafe_b64encode(urandom(12))[:12]
    v.value = value
    v.save()
    id = v.id
    return id, value

def user_verify_new(user_id, name, mail, cid):
    id, ck = _user_verify_new(user_id, cid)
    template = VERIFY_TEMPLATE[cid]
    mq_rendermail(template, mail, name, id=id, ck=ck)

def user_verify(id, value):
    v = UserVerify.get(id)
    if v:
        if v.value == value and v.create_time + TIME_LIMIT > time():
            return v.user_id, v.cid
    return 0, 0
