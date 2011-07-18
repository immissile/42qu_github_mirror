#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA
from txt import txt_property, txt_new
from gid import gid
from uuid import uuid4
from user_session import id_binary_encode, id_binary_decode
import binascii
from os import urandom
import time


class OauthAccessToken(Model):
    pass

class OauthClient(McModel):
    txt = txt_property

    @property
    def hex_secret(self):
        return binascii.hexlify(self.secret)

class OauthRefreshToken(Model):
    pass

def oauth_client_id_by_user_id(user_id):
    return OauthClient.where(user_id=user_id).order_by('id desc').col_list()

def oauth_client_by_user_id(user_id):
    return OauthClient.mc_get_list(oauth_client_id_by_user_id(user_id))

def oauth_client_new(user_id, name, txt):
    secret = uuid4().bytes
    id = gid()
    oauth_client = OauthClient(id, user_id=user_id, secret=secret)

    oauth_client.name = name
    txt_new(oauth_client.id, txt)
    oauth_client.save()
    hex_secret = binascii.hexlify(secret)
    return oauth_client

def oauth_secret(id):
    client = OauthClient.get(id)
    if client:
        return binascii.hexlify(client.secret)
    return 0

def oauth_access_token(client_id, user_id):
    u = OauthAccessToken.get(user_id=user_id, client_id=client_id)
    if u is not None:
        return u
    return False

def oauth_refresh_token(client_id, id):
    r = OauthRefreshToken.get(client_id=client_id, id=id)
    if r is not None:
        return r
    return False

def oauth_refresh_token_new(client_id, id):
    r = oauth_refresh_token(client_id, id)
    if not r:
        re = OauthRefreshToken.get_or_create(client_id=client_id, id=id)
        re.token = r = urandom(12)
        re.time = time.time()
        re.save()
    else:
        r = r.token
    return id_binary_encode(id, r)

def oauth_access_token_new(client_id, user_id):
    value = oauth_access_token(client_id, user_id)
    if not value:
        access = OauthAccessToken.get_or_create(user_id=user_id, client_id=client_id)
        access.token = value = urandom(12)
        access.save()
        id = access.id
    else :
        id = value.id
        value = value.token
    return id_binary_encode(id, value)

def oauth_access_token_verify(client_id, access_token):
    id, token = id_binary_decode(access_token)
    print id
    o = OauthAccessToken.get(client_id=client_id, token=token, id=id)
    if o:
        return o.user_id


