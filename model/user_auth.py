#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from hashlib import sha256
from user_mail import user_mail_new, user_id_by_mail
from zsite import zsite_new_user, Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_NO_PASSWORD
from binascii import hexlify

def hash_password(id, password):
    return sha256('%s%s'%(password, id)).digest()

class UserPassword(Model):
    pass

def user_password_sha256(user_id):
    password = UserPassword.get(id=user_id)
    if password:
        return hexlify(password.password)

def mail_password_verify(mail, password):
    user_id = user_id_by_mail(mail)
    if user_id:
        p = UserPassword.get(user_id)
        if p.password == hash_password(user_id, password):
            return True


def user_password_new(user_id, password):
    if password is not None:
        o = UserPassword.get_or_create(id=user_id)
        o.password = hash_password(user_id, password)
        o.save()


def user_password_verify(user_id, password):
    p = UserPassword.get(user_id)
    if p is None:
        user_password_new(user_id, password)
        return True
    if p.password == hash_password(user_id, password):
        return True

def user_new_by_mail(mail, password=None, name=None):
    if not name:
        name = mail.split('@', 1)[0].split('+', 1)[0]
        if name.isdigit():
            name = ''
    if password:
        state = ZSITE_STATE_APPLY
    else:
        state = ZSITE_STATE_NO_PASSWORD
    zsite = zsite_new_user(name, state)
    user_id = zsite.id
    user_mail_new(user_id, mail)
    if password:
        user_password_new(user_id, password)
    from buzz_sys import buzz_sys_new_user
    buzz_sys_new_user(user_id)
    return zsite


def newbie_redirect(user):
    if user.state == ZSITE_STATE_NO_PASSWORD:
        return '/i/guide'

if __name__ == '__main__':
    z = Zsite.mc_get(10001299)
    print z.sex, '!'
    print user_password_sha256(1)


