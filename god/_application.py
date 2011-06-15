#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.wsgi
import _url
from _urlmap import urlmap

application = tornado.wsgi.WSGIApplication(
    tuple(urlmap.handlers),
    login_url='/login',
)
