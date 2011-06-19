#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
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

mc_api_serect = McCache('ApiSerect:%s')

class ApiApp(Model):
    txt = txt_property

    @property
    def hex_serect(self):
        return binascii.hexlify(self.serect)

def api_app_new(user_id, name, txt):
    serect = uuid4().bytes
    id = gid()
    api_app = ApiApp(id, user_id=user_id, serect=serect)

    api_app.name = name
    txt_new(api_app.id, txt)
    api_app.save()
    hex_serect = binascii.hexlify(serect)
    mc_api_serect.set(id, hex_serect)
    return api_app

@mc_api_serect('{id}')
def api_serect(id):
    api = ApiApp.get(id)
    if api:
        return binascii.hexlify(app.serect)
    return 0



#生成的url
def app_url_encode(arguments):
    items = arguments.items()
    items.sort(key=itemgetter(0))
    return urlencode(items)


#生成签名
def api_sign(arguments, serect):
    _url = app_url_encode(arguments)
    url = '&'.join((_url, 'client_serect=%s'%serect))
    return sha256(url).hexdigest()


#服务器效验URL
def api_sign_verify(arguments):
    client_id = arguments['client_id']
    sign = arguments['sign']
    client_secret = api_serect(client_id)
    del arguments['sign']
    sign2 = api_sign(arguments, client_secret)

    if sign == sign2:
        return True


def auth_token(mail, password_sha256):
    mail = mail.strip().lower()
    password    


if __name__ == '__main__':
    api_app = ApiApp.get(73)
    serect = api_app.hex_serect
    print 'client_id', api_app.id
    print 'client_serect', serect
    arguments = {
        'client_id': api_app.id,
        'test':'abc',
        'test2':'123'
    }
    print 'arguments', arguments
    sign = app_sign(arguments, serect)
    print 'sign', sign
    arguments['sign'] = sign
    api_sign_verify(arguments)

