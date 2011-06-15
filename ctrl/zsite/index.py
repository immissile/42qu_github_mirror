#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zsite import  _handler
from _urlmap import urlmap

@urlmap('/')
class Index(_handler.Base):
    def get(self):
        self.render()
