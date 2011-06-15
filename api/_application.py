#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import _url
from _urlmap import urlmap

application = tornado.web.Application(
    tuple(urlmap.handlers)
)
