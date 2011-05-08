#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache

class UserMail(McModel):
    pass

mc_user_id_by_mail = McCache("UserIdByMail:%s")

def user_id_by_mail(mail):
    mail = mail.strip().lower()

    c = mc_user_id_by_mail.get(mail)
    if c:
        return c

    c = UserMail.raw_sql("select id from user_mail where mail=%s", mail).fetchone()
    if c:
        c = c[0]
    if not c:
        c = 0
    mc_user_id_by_mail.set(mail, c)
    return c


if __name__ == "__main__":
    print user_id_by_mail("zsp007@gmail.com")
