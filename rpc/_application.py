#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _url
from _urlmap import urlmap
import tornado.web

application = tornado.web.Application(
    tuple(urlmap.handlers)
)
