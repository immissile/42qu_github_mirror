#!/usr/bin/env python
#coding:utf-8


import _handler
from zweb._urlmap import urlmap

@urlmap('/')
class Index(_handler.Base):
    def get(self):
        self.render()

@urlmap('/chart')
class Chart(_handler.Base):
    def get(self):
        self.render()


