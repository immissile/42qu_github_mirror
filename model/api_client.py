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

mc_api_serect = McCache('ApiSerect:%s')
mc_api_session = McCache('ApiSession:%s')
mc_api_client_id_by_user_id = McCacheA('ApiClientIdByUserId:%s')

class ApiSession(Model):
    pass

class ApiClient(McModel):
    txt = txt_property

    @property
    def hex_serect(self):
        return binascii.hexlify(self.serect)

@mc_api_client_id_by_user_id('{user_id}')
def api_client_id_by_user_id(user_id):
    return ApiClient.where(user_id=user_id).order_by('id desc').col_list()


def api_client_by_user_id(user_id):
    return ApiClient.mc_get_list(api_client_id_by_user_id(user_id))

def api_client_new(user_id, name, txt):
    serect = uuid4().bytes
    id = gid()
    api_client = ApiClient(id, user_id=user_id, serect=serect)

    api_client.name = name
    txt_new(api_client.id, txt)
    api_client.save()
    hex_serect = binascii.hexlify(serect)
    mc_api_serect.set(id, hex_serect)
    mc_api_client_id_by_user_id.delete(user_id)
    return api_client

@mc_api_serect('{id}')
def api_serect(id):
    client = ApiClient.get(id)
    if client:
        return binascii.hexlify(client.serect)
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

def _api_sign(arguments, serect):
    _url = client_url_encode(arguments)
    url = '&'.join((_url, 'client_serect=%s'%serect))
#    print url
    return sha256(url).hexdigest(), _url

#生成签名
def api_sign(arguments, serect):
    return _api_sign(arguments, serect)[0]

#服务器效验URL
def api_sign_verify(arguments):
    client_id = arguments['client_id']
    sign = arguments['sign']
    client_secret = api_serect(client_id)
    del arguments['sign']
    sign2 = api_sign(arguments, client_secret)
    if sign == sign2:
        return True

#生成已经签名了的参数
def api_sign_arguments(arguments, serect):
    sign, url = _api_sign(arguments, serect)
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
    client_id, serect,
    user_id, mail, password
):
    arguments = dict(
        user_id=user_id,
        client_id=client_id,
        mail=mail,
        token=api_login_token(user_id, mail, password)
    )
    url = api_sign_arguments(arguments, serect)
    return '%s/user/auth/login?%s'%(API_URL, url)

def api_s_url(client_id, serect, s, url, **kwds):
    arguments = kwds
    kwds['client_id'] = client_id
    kwds['S'] = s
    return '%s%s?%s'%(API_URL, url, api_sign_arguments(arguments, serect))

if __name__ == '__main__':
    api_client = ApiClient.get(73)
    #  serect = api_client.hex_serect
    #  print 'client_id', api_client.id
    #  print 'client_serect', serect


#    print api_client_id_by_user_id(1)
#    for i in ApiClient.where(user_id=1):
#    print api_session_new(client_id, user_id)
#        print i
#    print ApiClient.where(user_id=1).order_by('id desc').col_list()
#    print api_client_by_user_id(1)
#    mc_api_client_id_by_user_id.delete(1)
    client_id = 73
    serect = 'beafcff6034e4b26b914241235e66da4'
    user_id = 74
    mail = 'test@42qu.com'
    password = '123456'


    arguments = {
        'client_id': client_id,
        'test':'abc',
        'test2':'123'
    }
#    print api_sign(arguments, serect)
    #print 'arguments', arguments
    #sign = api_sign(arguments, serect)
    #print 'sign', sign
    #arguments['sign'] = sign
    #api_sign_verify(arguments)



    print api_s_url(
        client_id, serect, 'SgAAAA7QQDfo6x7oUPcjSA', '/po/rm', po_id='abc', test2='123'
    )
#  http://api.42qu.me/user/auth/login?client_id=6&mail=yuri.ted%40gmail.com&sign=6a09d455ca8f739940ae70786b2126587a62524ca5ab2dcfbf4d53e76c1fc6f0&token=f8d9fd667733d97be073350f7df4a3dd77eb414ef355277d4f504dbce3dbedc0


