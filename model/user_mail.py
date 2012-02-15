#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from model.zsite import Zsite

MAIL_UNVERIFY = 40
MAIL_VERIFIED = 50
MAIL_LOGIN = 60


class UserMail(Model):
    pass

mc_mail_by_user_id = McCache('MailByUserId.%s')
#mc_mail_by_user_id_if_login = McCache('MailByUserIdIfLogin.%s')

#@mc_mail_by_user_id_if_login('{user_id}')
#def mail_by_user_id_if_login(user_id):
#    c = UserMail.raw_sql('select mail from user_mail where user_id=%s and state=%s', user_id, MAIL_LOGIN).fetchone()
#    if c:
#        return c[0]
#    return ''

@mc_mail_by_user_id('{user_id}')
def mail_by_user_id(user_id):
    c = UserMail.raw_sql('select mail from user_mail where user_id=%s order by state desc limit 1', user_id).fetchone()
    if c:
        return c[0]
    return ''


mc_user_id_by_mail = McCache('UserIdByMail:%s')

@mc_user_id_by_mail('{mail}')
def _user_id_by_mail(mail):
    c = UserMail.raw_sql('select user_id from user_mail where mail=%s ', mail).fetchone()
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

def user_mail_new(user_id, mail, state=MAIL_UNVERIFY):
    mail = mail.strip().lower()
    id = user_id_by_mail(mail)
    if  id and id != user_id:
        return False

    if state == MAIL_UNVERIFY:
        UserMail.where(user_id=user_id, state=MAIL_UNVERIFY).delete()

    u = UserMail(mail=mail, user_id=user_id, state=state)
    u.save()
    mc_mail_by_user_id.set(user_id, mail)
    mc_user_id_by_mail.set(mail, user_id)
    return user_id

def user_mail_active_by_user_id(user_id, mail=None):
    for u in UserMail.where(user_id=user_id, state=MAIL_LOGIN):
        u.state = MAIL_VERIFIED
        u.save()

    um = None
    if not mail:
        um = UserMail.get(user_id=user_id, state=MAIL_UNVERIFY)
        mail = um.mail
    else:
        um = UserMail.get(user_id=user_id, mail=mail)

    if um is not None:
        um.state = MAIL_LOGIN
        um.save()
        mc_mail_by_user_id.set(user_id, mail)
        mc_user_id_by_mail.set(mail, user_id)

    return um

def user_mail_by_state(user_id, state):
    return UserMail.where(user_id=user_id).where('state>=%s', state).col_list(col='mail')

if __name__ == '__main__':
    #pass
    #from zsite import Zsite, CID_USER, STATE_ACTIVE
    #for i in Zsite.where(cid=CID_USER).where("state>=%s"%STATE_ACTIVE):
    #    print i.id
    print mail_by_user_id(10079424)


