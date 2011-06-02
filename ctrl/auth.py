#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from cgi import escape
from model.cid import CID_VERIFY_MAIL
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.zsite import ZSITE_STATE_APPLY

@urlmap('/logout')
class Logout(_handler.Base):
    def get(self):
        self.clear_cookie('S')
        current_user = self.current_user
        if current_user:
            user_session_rm(current_user.id)
        self.redirect('/')

@urlmap('/login')
class Login(_handler.Base):
    def get(self):
        if self.current_user:
            return self.redirect('/')
        self.render()

    def _login(self, user_id, mail, redirect):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        self.redirect(redirect)

    def post(self):
        mail = self.get_argument('mail', None)
        password = self.get_argument('password', None)

        error_mail = None
        error_password = None

        if mail:
            mail = mail.lower()
        if not mail:
            error_mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            error_mail = '邮箱格式有误'

        if not password:
            error_password = '请输入密码'

        if not any((error_password, error_mail)):
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    return self._login(user_id, mail, self.get_argument('next', '/'))
                else:
                    error_password = '密码有误。忘记密码了？<a href="/password/%s">点此找回</a>' % escape(mail)
            else:
                user_id = user_new_by_mail(mail, password)
                return self._login(user_id, mail, '/verify/mail')

        self.render(
            mail=mail,
            password=password,
            error_mail=error_mail,
            error_password=error_password,
        )

@urlmap('/password')
class Password(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        user_id = self.current_user_id
        password0 = self.get_argument('password0', None)
        password = self.get_argument('password', None)
        password2 = self.get_argument('password2', None)

        if all((password0, password, password2)) and password == password2:
            if user_password_verify(user_id, password0):
                user_password_new(user_id, password)
                success = True
            else:
                error_password = '密码有误。忘记密码了？<a href="/password/%s">点此找回</a>' % escape(mail)
        self.render(success=success)
