#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache

class UserMail(Model):
    pass

mc_user_id_by_mail = McCache("UserIdByMail:%s")

@mc_user_id_by_mail('{mail}')
def _user_id_by_mail(mail):
    c = UserMail.raw_sql("select user_id from user_mail where mail=%s", mail).fetchone()
    if c:
        return c[0]
    return 0

def user_id_by_mail(mail):
    mail = mail.strip().lower()
    return _user_id_by_mail(mail)

def user_mail_new(user_id, mail):
    mail = mail.strip().lower()
    user_id = user_id_by_mail(mail)
    if user_id:
        return user_id
    u = UserMail(mail=mail,user_id=user_id)
    u.save()
    mc_user_id_by_mail.set(mail, user_id)
    return user_id

if __name__ == "__main__":
    for i in UserMail.where():
        i.delete()
    #print user_id_by_mail_new("zsp007@gmail.com")
