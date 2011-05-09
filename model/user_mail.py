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

def user_mail_new(user_id, mail):
    mail = mail.strip().lower()
    id = user_id_by_mail(mail)
    if id:
        return id
    u = UserMail(mail=mail)
    u.save()
    id = u.id
    mc_user_id_by_mail.set(mail, id)
    return id

if __name__ == "__main__":
    for i in UserMail.where():
        i.delete()
    #print user_id_by_mail_new("zsp007@gmail.com")
