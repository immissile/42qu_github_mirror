#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap


@urlmap("/login")
class Login(_handler.Base):
    def get(self):
        self.render()

    def post(self):
        mail = self.get_argument('mail',None)
        password = self.get_argument('password',None)
        if mail and password:

        self.render(
            mail = mail,
            password = password
        )

