#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap

@urlmap('/po/word')
class Index(_handler.ApiLoginBase):
    def get(self):
        result = {}
        self.finish(result)

