#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import _urlmap
from zweb import _urlmap

application = tornado.web.Application(
    tuple(_urlmap.URLMAP)
)
