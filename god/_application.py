#!/usr/bin/env python
#coding:utf-8

import tornado.wsgi
from zweb import _urlmap
application = tornado.wsgi.WSGIApplication(
    tuple(_urlmap.URLMAP) ,
    login_url="/login",
)


