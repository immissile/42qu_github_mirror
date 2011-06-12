#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.wsgi
import main
import zsite

from zweb._urlmap import URLMAP

application = tornado.wsgi.WSGIApplication(
    tuple(URLMAP),
    login_url='/login',
    xsrf_cookies=True,
)
