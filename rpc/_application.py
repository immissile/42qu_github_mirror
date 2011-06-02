#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from zweb import _urlmap

application = tornado.web.Application(
    tuple(_urlmap.URLMAP)
)
