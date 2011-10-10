#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import _url
from _urlmap import urlmap
from config import SITE_URL

application = tornado.web.Application(
    tuple(urlmap.handlers),
    login_url='%s/auth/login'%SITE_URL
)
