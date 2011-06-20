#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.wsgi
import model._db
import _url
from _urlmap import urlmap
from config import SITE_URL

application = tornado.wsgi.WSGIApplication(
    tuple(urlmap.handlers),
    login_url='%s/login' % SITE_URL,
)
