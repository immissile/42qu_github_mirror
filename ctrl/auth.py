#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from zkit.txt import EMAIL_VALID
from cgi import escape

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

        if not any((error_password,error_mail)):
            error_password = """密码有误。 忘记密码了？<a href="/password/reset/%s">点此找回</a>"""%escape(mail)

        self.render(
            mail = mail,
            password = password,
            error_mail = error_mail,
            error_password = error_password
        )


@urlmap("/password/reset/(.*)")
class PasswordReset(_handler.Base):
    pass


