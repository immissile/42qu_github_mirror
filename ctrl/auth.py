#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap


@urlmap("/login")
class Login(_handler.Base):
    def get(self):
        self.render(test="test")

    def post(self):
        mail = self.get_argument('mail')
        password = self.get_argument('password')
        print mail,password
        self.render()

