#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()
