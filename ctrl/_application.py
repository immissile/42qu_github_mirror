#!/usr/bin/env python
# -*- coding: utf-8 -*-
import main
import zsite
import index

from zweb._urlmap import URLMAP
import tornado.wsgi

application = tornado.wsgi.WSGIApplication(
    tuple(URLMAP),
    login_url='/login',
    xsrf_cookies=True,
)
