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

mc_oauth_client_id_by_user_id = McCacheA('OauthClientIdListByUserId.%s')

@mc_oauth_client_id_by_user_id('{user_id}')
def oauth_client_id_by_user_id(user_id):
    return OauthClient.where(user_id=user_id).order_by('id desc').col_list()

def oauth_client_by_user_id(user_id):
    return OauthClient.mc_get_list(oauth_client_id_by_user_id(user_id))

def oauth_client_new(user_id, name, txt):
    secret = uuid4().bytes
    id = gid()
    o = OauthClient(id=id, user_id=user_id, secret=secret, name=name)
    o.save()

    txt_new(id, txt)
    mc_oauth_client_id_by_user_id.delete(user_id)
    return o

def oauth_secret(id):
    client = OauthClient.mc_get(id)
    if client:
        return binascii.hexlify(client.secret)
    return 0

def oauth_access_token(client_id, user_id):
    o = OauthAccessToken.get(user_id=user_id, client_id=client_id)
    if o:
        return o

def oauth_refresh_token(client_id, id):
    o = OauthRefreshToken.get(client_id=client_id, id=id)
    if o:
        return o

def oauth_refresh_token_new(client_id, id):
    o = oauth_refresh_token(client_id, id)
    if not o:
        o = OauthRefreshToken.get_or_create(client_id=client_id, id=id)
        o.token = urandom(12)
        o.time = time.time()
        o.save()
    return id_binary_encode(id, o.token)

def oauth_access_token_new(client_id, user_id):
    o = oauth_access_token(client_id, user_id)
    if not o:
        o = OauthAccessToken.get_or_create(user_id=user_id, client_id=client_id)
        o.token = urandom(12)
        o.save()
    id = o.id
    access_token = id_binary_encode(id, o.token)
    mc_oauth_access_token_verify.delete(access_token)
    return id, access_token

mc_oauth_access_token_verify = McCacheA('OauthAccessTokenVerify.%s')

@mc_oauth_access_token_verify('{access_token}')
def _oauth_access_token_verify(access_token):
    id, token = id_binary_decode(access_token)
    o = OauthAccessToken.get(id)
    if o and o.token == token:
        return o.client_id, o.user_id
    return 0, 0

def oauth_access_token_verify(client_id, access_token):
    client_id = int(client_id)
    if client_id:
        _client_id, user_id = _oauth_access_token_verify(access_token)
        if client_id == _client_id:
            return user_id
    return 0
