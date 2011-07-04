#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from time import time
from model.mail import rendermail
from model.cid import CID_VERIFY_MAIL
from model.user_mail import mail_by_user_id
from model.verify import VERIFY_TEMPLATE, Verify

TIME_LIMIT = 3600 * 24 * 7

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
        item.update(create_time = now)


if __name__=='__main__':
    re_send_verify()
