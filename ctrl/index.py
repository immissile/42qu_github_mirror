#!/usr/bin/env python
#coding:utf-8


from zweb import _handler
from zweb._urlmap import urlmap


@urlmap("/")
class Index(_handler.Base):
    def get(self):
        self.render(test="test")


