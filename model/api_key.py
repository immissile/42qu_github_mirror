#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from hashlib import sha256
from user_mail import user_mail_new, user_id_by_mail
from zsite import zsite_new_user, Zsite
from txt import txt_property, txt_new
from gid import gid
from uuid import uuid4
from _db import McCache
from urllib import urlencode
import binascii


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
def app_serect(id):
    app = ApiApp.get(id)
    if app:
        return binascii.hexlify(app.serect)
    return 0


def api_sign(key, serect):
    pass


if __name__ == '__main__':
    #api_app = api_app_new(1, 'x', 'x')
    #print api_app.id
    print app_serect(46)



