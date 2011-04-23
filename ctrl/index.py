#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap


@urlmap("/")
class IndexHandler(_handler.Handler):
    def get(self):
        self.write("Hello, world2")
        raise


