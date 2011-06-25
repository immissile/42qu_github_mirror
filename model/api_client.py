#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCacheA
from os import urandom
from user_mail import user_mail_new, user_id_by_mail
from zsite import zsite_new_user, Zsite
from txt import txt_property, txt_new
from gid import gid
from uuid import uuid4
from _db import McCache
from urllib import urlencode
from hashlib import sha256
import binascii
from operator import itemgetter
from config import SITE_DOMAIN
from user_session import password_encode, user_id_value_by_session

API_URL = 'http://api.%s'%SITE_DOMAIN

mc_api_secret = McCache('ApiSerect:%s')
mc_api_session = McCache('ApiSession:%s')
mc_api_client_id_by_user_id = McCacheA('ApiClientIdByUserId:%s')

class ApiSession(Model):
    pass

class ApiClient(McModel):
    txt = txt_property

    @property
    def hex_secret(self):
        return binascii.hexlify(self.secret)

@mc_api_client_id_by_user_id('{user_id}')
def api_client_id_by_user_id(user_id):
    return ApiClient.where(user_id=user_id).order_by('id desc').col_list()


def api_client_by_user_id(user_id):
    return ApiClient.mc_get_list(api_client_id_by_user_id(user_id))

def api_client_new(user_id, name, txt):
    secret = uuid4().bytes
    id = gid()
    api_client = ApiClient(id, user_id=user_id, secret=secret)

    api_client.name = name
    txt_new(api_client.id, txt)
    api_client.save()
    hex_secret = binascii.hexlify(secret)
    mc_api_secret.set(id, hex_secret)
    mc_api_client_id_by_user_id.delete(user_id)
    return api_client

@mc_api_secret('{id}')
def api_secret(id):
    client = ApiClient.get(id)
    if client:
        return binascii.hexlify(client.secret)
    return 0

@mc_api_session('{client_id}_{user_id}')
def api_session(client_id, user_id):
    u = ApiSession.get(user_id=user_id, client_id=client_id)
    if u is not None:
        return u.value or False
    return False

def api_session_new(client_id, user_id):
    value = api_session(client_id, user_id)
    if not value:
        session = ApiSession.get_or_create(user_id=user_id, client_id=client_id)
        session.value = value = urandom(12)
        session.save()
        mc_api_session.set('%s_%s'%(client_id, user_id), session.value)
    return password_encode(user_id, value)

#生成的url
def client_url_encode(arguments):
    items = arguments.items()
    items.sort(key=itemgetter(0))
    return urlencode(items)

def _api_sign(arguments, secret):
    _url = client_url_encode(arguments)
    url = '&'.join((_url, 'client_secret=%s'%secret))
    #print url
    return sha256(url).hexdigest(), _url

#生成签名
def api_sign(arguments, secret):
    url = _api_sign(arguments, secret)[0]
    return url

#服务器效验URL
def api_sign_verify(arguments):
    client_id = arguments['client_id']
    sign = arguments['sign']
    client_secret = api_secret(client_id)
    del arguments['sign']
    sign2 = api_sign(arguments, client_secret)
    if sign == sign2:
        return True

#生成已经签名了的参数
def api_sign_arguments(arguments, secret):
    sign, url = _api_sign(arguments, secret)
    return '%s&sign=%s'%(url, sign)

def api_login_verify(client_id, s):
    user_id, session = user_id_value_by_session(s)
    if not user_id:
        return
    session2 = api_session(client_id, user_id)
    #print session2,"!!!", client_id, user_id
    if session != session2:
        return
    return user_id

######## 以下为客户端生成URL的演示部分 #########

def api_login_token(user_id, mail, password):
    mail = mail.strip().lower()
    password = password.strip()
    hexdigest = sha256(password+str(user_id)).hexdigest()
    return sha256(mail+hexdigest).hexdigest()

def api_login_url(
    client_id, secret,
    user_id, mail, password
):
    arguments = dict(
        user_id=user_id,
        client_id=client_id,
        mail=mail,
        token=api_login_token(user_id, mail, password)
    )
    url = api_sign_arguments(arguments, secret)
    return '%s/user/auth/login?%s'%(API_URL, url)

def api_s_url(client_id, secret, s, url, **kwds):
    arguments = kwds
    kwds['client_id'] = client_id
    kwds['S'] = s
    return '%s%s?%s'%(API_URL, url, api_sign_arguments(arguments, secret))

if __name__ == '__main__':
    api_client = ApiClient.get(73)
    #  secret = api_client.hex_secret
    #  print 'client_id', api_client.id
    #  print 'client_secret', secret


#    print api_client_id_by_user_id(1)
#    for i in ApiClient.where(user_id=1):
#    print api_session_new(client_id, user_id)
#        print i
#    print ApiClient.where(user_id=1).order_by('id desc').col_list()
#    print api_client_by_user_id(1)
#    mc_api_client_id_by_user_id.delete(1)
    client_id = 422
    #secret = '0c8bce6c05ae4f85a54d07230db1720a'
    secret = 'beafcff6034e4b26b914241235e66da4'
    user_id = 79
    mail = 'yupbank@qq.com'
    password = '6171446'


    arguments = {
        'client_id': client_id,
        'test':'abc',
        'test2':'123'
    }

    print api_sign_arguments(arguments, secret)
    #print 'arguments', arguments
    #sign = api_sign(arguments, secret)
    #print 'sign', sign
    #arguments['sign'] = sign
    #api_sign_verify(arguments)
    #print api_session_new(client_id, user_id)



#    print api_s_url(
#        client_id, secret, 'TwAAAAJLXJwwusxtJBjpAK', '/po/rm', po_id='427'
#    )
#  http://api.42qu.me/user/auth/login?client_id=6&mail=yuri.ted%40gmail.com&sign=6a09d455ca8f739940ae70786b2126587a62524ca5ab2dcfbf4d53e76c1fc6f0&token=f8d9fd667733d97be073350f7df4a3dd77eb414ef355277d4f504dbce3dbedc0


