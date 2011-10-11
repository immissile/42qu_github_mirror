#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase
from _urlmap import urlmap


@urlmap('/')
class Index(LoginBase):
    def get(self):
        self.finish('it works')
