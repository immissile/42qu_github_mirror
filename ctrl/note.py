#!/usr/bin/env python
#coding:utf-8


import _handler
from zweb._urlmap import urlmap

@urlmap("/note/write")
class write(_handler.Base):
    def get(self):
        return self.render()
