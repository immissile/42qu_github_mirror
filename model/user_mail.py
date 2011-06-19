#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from model.zsite import Zsite

class UserMail(Model):
    pass

mc_mail_by_user_id = McCache('MailByUserId.%s')

@mc_mail_by_user_id('{user_id}')
def mail_by_user_id(user_id):
    c = UserMail.raw_sql('select mail from user_mail where user_id=%s', user_id).fetchone()
    if c:
        return c[0]
    return ''

mc_user_id_by_mail = McCache('UserIdByMail:%s')

@mc_user_id_by_mail('{mail}')
def _user_id_by_mail(mail):
    c = UserMail.raw_sql('select user_id from user_mail where mail=%s', mail).fetchone()
    if c:
        return c[0]
    return 0

def user_by_mail(mail):
    user_id = user_id_by_mail(mail)
    return Zsite.mc_get(user_id)

def user_id_by_mail(mail):
    if mail:
        mail = mail.strip().lower()
        return _user_id_by_mail(mail)

def user_mail_new(user_id, mail):
    mail = mail.strip().lower()
    id = user_id_by_mail(mail)
    if id:
        return id
    u = UserMail(mail=mail, user_id=user_id)
    u.save()
    mc_mail_by_user_id.set(user_id, mail)
    mc_user_id_by_mail.set(mail, user_id)
    return user_id

if __name__ == '__main__':
    for i in UserMail.where():
        i.delete()
