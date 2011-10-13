#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase
from _urlmap import urlmap


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap('/auth/login')
class AuthLogin(Base):
    def get(self):
        self.render(
                errtip = Errtip()
                )
