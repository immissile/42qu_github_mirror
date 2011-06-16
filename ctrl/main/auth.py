# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.auth import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from cgi import escape
from model.cid import CID_VERIFY_MAIL
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.zsite import ZSITE_STATE_APPLY

@urlmap('/logout')
class Logout(Base):
    def get(self):
        self.clear_cookie('S')
        current_user = self.current_user
        if current_user:
            user_session_rm(current_user.id)
        self.redirect('/')

@urlmap('/login')
class Login(Base):
    def get(self):
        current_user = self.current_user
        if current_user:
            return self.redirect('%s/live'%current_user.link)
        self.render()

    def _login(self, user_id, mail, redirect):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if redirect:
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
                    return self._login(user_id, mail, self.get_argument('next', None))
                else:
                    error_password = '密码有误。忘记密码了？<a href="/password/%s">点此找回</a>' % escape(mail)
            else:
                user_id = user_new_by_mail(mail, password)
                return self._login(user_id, mail, '/auth/verify/mail')

        self.render(
            mail=mail,
            password=password,
            error_mail=error_mail,
            error_password=error_password,
        )

@urlmap('/password')
class Password(LoginBase):
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



from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.me import urlmap
from zkit.txt import EMAIL_VALID, mail2link
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.user_auth import user_password_new
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from model.user_session import user_session

@urlmap('/auth/verify/mail')
class Mail(LoginBase):
    cid = CID_VERIFY_MAIL
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        if current_user.state == ZSITE_STATE_APPLY:
            mail = mail_by_user_id(current_user_id)
            verify_mail_new(current_user_id, current_user.name, mail, self.cid)
            link = mail2link(mail)
            return self.render(
                mail=mail,
                link=link,
            )
        self.redirect('/')

class VerifyBase(Base):
    cid = None
    def handler_verify(self, id, ck, delete=False):
        user_id, cid = verifyed(id, ck, delete)
        if user_id and self.cid == cid:
            session = user_session(user_id)
            self.set_cookie('S', session)
            return user_id
        else:
            self.redirect('/')

@urlmap('/auth/verify/mail/(\d+)/(.+)')
class VerifyMail(VerifyBase):
    cid = CID_VERIFY_MAIL
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            user = Zsite.mc_get(user_id)
            if user.state == ZSITE_STATE_APPLY:
                user.state = ZSITE_STATE_ACTIVE
                user.save()
            self.render()

@urlmap('/password/(.+)')
class Password(Base):
    cid = CID_VERIFY_PASSWORD
    def get(self, mail):
        if EMAIL_VALID.match(mail):
            user_id = user_id_by_mail(mail)
            if user_id:
                user = Zsite.mc_get(user_id)
                verify_mail_new(user_id, user.name, mail, self.cid)
                link = mail2link(mail)
                return self.render(
                    mail=mail,
                    link=link,
                )
        self.redirect('/')

@urlmap('/auth/verify/password/(\d+)/(.+)')
class VerifyPassword(VerifyBase):
    cid = CID_VERIFY_PASSWORD
    def get(self, id, ck):
        user_id = self.handler_verify(id, ck)
        if user_id:
            self.render()

    def post(self, id, ck):
        current_user_id = self.current_user_id
        if current_user_id:
            password = self.get_argument('password', None)
            if password:
                user_id = self.handler_verify(id, ck, True)
                if current_user_id == user_id:
                    user_password_new(user_id, password)
                    return self.render(password=password)
            else:
                return self.get(id, ck)
        self.redirect('/')
