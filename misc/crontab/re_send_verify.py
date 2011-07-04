#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from time import time
from model.mail import rendermail
from model.user_mail import mail_by_user_id
from model.verify import VERIFY_TEMPLATE, Verify
from model.days import today_days

SIX_DAYS = 3600 * 24 * 6 
A_DAY = 3600 * 24

def re_send_verify():
    today = today_days() * A_DAY
    ago = today - SIX_DAYS
    week_ago = ago - A_DAY
    for item in Verify.where('create_time<%s and create_time>%s', ago, week_ago):
        mail = mail_by_user_id(item.user_id)
        name = mail
        ck = item.value
        id = item.user_id
        template = '/mail/auth/verify/miss.txt'
        rendermail(template, mail, name, id=id, ck=ck)


if __name__=='__main__':
    re_send_verify()
