#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from time import time
from model._db import Model, McModel, McCache, mc, cursor_by_table
from model.mail import rendermail
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD, CID_VERIFY_MONEY
from model.user_mail import mail_by_user_id


TIME_LIMIT = 3600 * 24 * 7

VERIFY_TEMPLATE = {
    CID_VERIFY_MAIL: '/mail/auth/verify/mail.txt',
}

class Verify(Model):
    pass

def re_send_verify():
    import time
    now = int(time.time())
    week_ago = now - TIME_LIMIT
    for item in Verify.where('create_time<%s'%week_ago):
        mail = mail_by_user_id(item.user_id)
        name = mail
        ck = item.value
        id = item.user_id
        template = VERIFY_TEMPLATE[CID_VERIFY_MAIL]
        rendermail(template, mail, name, id=id, ck=ck)
        item.create_time = now
        item.save()
        


if __name__=='__main__':
    re_send_verify()
