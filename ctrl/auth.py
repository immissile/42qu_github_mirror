#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from zkit.txt import EMAIL_VALID

@urlmap("/login")
class Login(_handler.Base):
    def get(self):
        self.render()

    def post(self):
        mail = self.get_argument('mail',None)
        password = self.get_argument('password',None)

        error_mail = None
        error_password = None

        if mail:
            mail = mail.strip().lower()
        if not mail:
            error_mail = "请输入邮箱"
        elif not EMAIL_VALID.match(mail):
            error_mail = "邮箱格式有误"

        if not password:
            error_password = "请输入密码"


        self.render(
            mail = mail,
            password = password,
            error_mail = error_mail,
            error_password = error_password
        )

