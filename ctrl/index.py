#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap


@urlmap("/")
class Index(_handler.Base):
    def get(self):
        #print self.headers
        self.render(test="test")


