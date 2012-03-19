#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite import Zsite, ZSITE_STATE_VERIFY, ZSITE_STATE_APPLY
from model.user_mail import UserMail, MAIL_LOGIN, MAIL_UNVERIFY


def check():
    for z in Zsite.where():
        um = UserMail.get(user_id=z.id)
        print z.id
        if um:
            if z.state <= ZSITE_STATE_APPLY:
                um.state = MAIL_UNVERIFY
                um.save()
            else:
                um.state = MAIL_LOGIN
                um.save()

if __name__ == '__main__':
    check()
