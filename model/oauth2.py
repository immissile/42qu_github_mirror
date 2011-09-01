#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA
from kv import Kv
from txt import txt_property, txt_new
from gid import gid
from uuid import uuid4
from user_session import id_binary_encode, id_binary_decode
import binascii
from os import urandom
import time

oauth_client_uri = Kv('oauth_client_uri')

oauth_authorize_code = Kv('oauth_authorize_code')

mc_oauth_client_id_by_user_id = McCacheA('OauthClientIdListByUserId.%s')

mc_oauth_access_token_verify = McCache('OauthAccessTokenVerify.%s')



class OauthAccessToken(Model):
    pass

class OauthClient(McModel):
    txt = txt_property

    @property
    def hex_secret(self):
        return binascii.hexlify(self.secret)

    def rm(self):
        if self.cid:
            oauth_client_uri.delete(self.id)
        mc_oauth_client_id_by_user_id.delete(self.user_id)
        self.delete()

    def can_admin(self, user_id):
        return self.user_id == user_id 


class OauthRefreshToken(Model):
    pass


@mc_oauth_client_id_by_user_id('{user_id}')
def oauth_client_id_by_user_id(user_id):
    return OauthClient.where(user_id=user_id).order_by('id desc').col_list()

def oauth_access_token_by_user_id(user_id):
    return OauthAccessToken.where(user_id=user_id).order_by('client_id desc')

def oauth_client_by_user_id(user_id):
    oc = OauthClient.mc_get_list(oauth_client_id_by_user_id(user_id))
    for c in oc:
        if oauth_client_uri.get(c.id):
            c.uri = oauth_client_uri.get(c.id)
        else:
            c.uri = False
    return oc


def oauth_client_new(user_id, name, txt, site, cid=0):
    secret = uuid4().bytes
    id = gid()
    o = OauthClient(id=id, user_id=user_id, secret=secret, name=name, site=site, cid=cid)
    o.save()
    txt_new(id, txt)
    mc_oauth_client_id_by_user_id.delete(user_id)
    return o

def oauth_client_web_new(user_id, name, txt, uri, site, cid=0):
    o = oauth_client_new(user_id, name, txt, site, cid)
    oauth_client_uri.set(id=o.id, value=uri)
    return o

def oauth_client_edit(oauth_client_id, name, txt, site):
    o = OauthClient.mc_get(oauth_client_id)
    if name:
        o.name = name
    o.site = site
    o.save()
    txt_new(oauth_client_id, txt)
    mc_oauth_client_id_by_user_id.delete(o.user_id)
    return o

def oauth_client_web_edit(oauth_client_id, name, txt, site, uri):
    o = oauth_client_edit(oauth_client_id, name, txt, site)
    oauth_client_uri.set(o.id, uri)
    return o

def oauth_secret(id):
    client = OauthClient.mc_get(id)
    if client:
        return client.hex_secret
    return 0

def oauth_secret_verify(id, secret):
    client = OauthClient.mc_get(id)
    if client and id:
        if client.hex_secret == secret:
            return True
        return 0


def oauth_token_rm_if_can(id,user_id):
    o = OauthAccessToken.get(id=id)
    if o:
        if o.user_id == user_id:
            access_token = id_binary_encode(o.id, o.token)
            o.delete()
            mc_oauth_access_token_verify.delete(access_token)
            oauth_refresh_token_rm(id)

def oauth_refresh_token_rm(id):
    return OauthRefreshToken.where(id=id).delete()

def oauth_access_token(client_id, user_id):
    o = OauthAccessToken.get(user_id=user_id, client_id=client_id)
    if o:
        return o

def oauth_refresh_token(client_id, id):
    o = OauthRefreshToken.get(client_id=client_id, id=id)
    if o:
        return o

def oauth_authorize_code_new():
    value = urandom(12)
    id = oauth_authorize_code.insert_no_value_cache(value)
    return id_binary_encode(id, value)

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
    #print o.id , o.client_id

    access_token = id_binary_encode(id, o.token)
    mc_oauth_access_token_verify.delete(access_token)
    return id, access_token


@mc_oauth_access_token_verify('{access_token}')
def oauth_access_token_verify(access_token):
    id, token = id_binary_decode(access_token)
    o = OauthAccessToken.get(id)
    if o and o.token == token:
        return o.user_id
    return 0

def oauth_authorize_code_rm(id):
    oauth_authorize_code.delete(id)

def oauth_authorization_code_verify(authorization_code):
    id, code = id_binary_decode(authorization_code)
    t = oauth_authorize_code.get(id)
    if t and t == code:
        return id
    return 0


if __name__ == "__main__":
    from zweb.orm import ormiter
    for i in ormiter(OauthClient):
        print i
        if oauth_client_uri.get(i.id):
            print i
            i.cid = 1
            i.save()
