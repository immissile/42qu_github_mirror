#!/usr/bin/env python
#coding:utf-8


from zweb._handler.me import Base, LoginBase
from _urlmap import urlmap


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap("/apply")
def Apply(LoginBase):
    def get(self):
        self.render()
