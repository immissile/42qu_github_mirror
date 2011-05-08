#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from os import urandom
from struct import pack, unpack
from base64 import urlsafe_b64encode, urlsafe_b64decode

mc_user_session = McCache("UserSession:%s")

class UserSession(McModel):
    pass

@mc_user_session("{user_id}")
def user_session_by_db(user_id):
    u = UserSession.get(user_id)
    if u is not None:
        s = u.value
        return s

def user_session(user_id):
    s = user_session_by_db(user_id)
    if s is None:
        u = UserSession.get_or_create(id=user_id)
        if u.value is None:
            s = urandom(12)
            u.value = s
            u.save()
        mc.set(mc_key, s)

    user_id_key = pack("I", int(user_id))
    user_id_key = urlsafe_b64encode(user_id_key)[:6]

    ck_key = urlsafe_b64encode(s)
    return "%s%s"%(user_id_key, ck_key)

if __name__ == "__main__":
    print user_session(1)
