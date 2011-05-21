#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, mc, cursor_by_table
from os import urandom
from struct import pack, unpack
from base64 import urlsafe_b64encode, urlsafe_b64decode
from time import time

mc_user_session = McCache("UserSession:%s")

class UserSession(Model):
    pass

@mc_user_session("{user_id}")
def user_session_by_db(user_id):
    u = UserSession.get(user_id)
    if u is not None:
        return u.value

def user_session(user_id):
    s = user_session_by_db(user_id)
    if s is None:
        u = UserSession.get_or_create(id=user_id)
        if u.value is None:
            s = urandom(12)
            u.value = s
            u.save()
            mc_user_session.set(user_id, s)
            cursor = cursor_by_table('user_login_time')
            cursor.execute( 'insert delay into user_login_time (user_id, create_time) values (%s, %s)', (user_id, int(time())) )
            cursor.connection.commit()

    user_id_key = pack("I", int(user_id))
    user_id_key = urlsafe_b64encode(user_id_key)[:6]
    ck_key = urlsafe_b64encode(s)
    return "%s%s"%(user_id_key, ck_key)


def user_session_rm(user_id):
    u = UserSession.where(id=user_id).update(value=None)
    mc_user_session.delete(user_id)


def user_id_by_session(session):
    if not session:
        return
    user_id = session[:6]
    value = session[6:]
    try:
        value = urlsafe_b64decode(value+"=")
        user_id = urlsafe_b64decode(user_id+"==")
    except (binascii.Error, exceptions.TypeError):
        return

    user_id = unpack('I', user_id)[0]
    db = user_session_by_db(user_id)
    if value == db:
        return user_id

if __name__ == "__main__":
    session = user_session(2)
    print session
    #print session
    #print user_id_by_session(session)
    #user_session_rm(2)
