#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from cgi import escape
from model.cid import CID_VERIFY_MAIL
from model.user_auth import user_password_verify, user_new_by_mail
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.user_verify import user_verify_new, user_verify
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

    def _login(self, user_id, redirect):
        session = user_session(user_id)
        self.set_cookie('S', session)
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
                    return self._login(user_id, self.get_argument('next', '/'))
                else:
                    error_password = '密码有误。忘记密码了？<a href="/password/reset/%s">点此找回</a>' % user_id
            else:
                user_id = user_new_by_mail(mail, password)
                return self._login(user_id, '/auth/user_verify/mail')

        self.render(
            mail=mail,
            password=password,
            error_mail=error_mail,
            error_password=error_password,
        )

@urlmap('/auth/user_verify/mail')
class UserVerifyMail(_handler.LoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        if current_user.state == ZSITE_STATE_APPLY:
            mail = mail_by_user_id(current_user_id)
            user_verify_new(current_user_id, current_user.name, mail, CID_VERIFY_MAIL)
            link = mail2link(mail)
            self.render(
                mail=mail,
                link=link,
            )
        else:
            self.redirect('/')

@urlmap('/auth/verify/(\d+)/(.+)')
class UserVerify(_handler.Base):
    def get(self, id, ck):
        user_id, cid = user_verify(id, ck)
        if user_id:
            session = user_session(user_id)
            self.set_cookie('S', session)
            self.render(cid=cid)
        else:
            self.redirect('/')

@urlmap('/password/reset/(.+)')
class PasswordReset(_handler.Base):
    pass
