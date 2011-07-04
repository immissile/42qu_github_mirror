#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from time import time
from model.mail import rendermail
from model.user_mail import mail_by_user_id
from model.verify import Verify
from model.days import today_days, DAY_SECOND
from model.zsite import Zsite, ZSITE_STATE_APPLY


def re_send_verify():
    today = today_days() * DAY_SECOND
    ago = today - DAY_SECOND * 6
    week_ago = ago - DAY_SECOND
    print ago, week_ago
    li = []
    for i in Verify.where('create_time>%s and create_time<%s', week_ago, ago):
        user_id = i.user_id
        user = Zsite.mc_get(user_id)
        if user and user.state == ZSITE_STATE_APPLY:
            name = user.name
            mail = mail_by_user_id(user_id)
            id = i.id
            ck = i.value
            template = '/mail/auth/verify/miss.txt'
            #rendermail(template, mail, name, id=id, ck=ck)


if __name__=='__main__':
    re_send_verify()
