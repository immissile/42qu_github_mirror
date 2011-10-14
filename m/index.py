#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from zkit.errtip import Errtip
from zkit.txt import EMAIL_VALID, mail2link
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.zsite import Zsite
from cgi import escape
LOGIN_REDIRECT = '/'

class NoLoginBase(Base):
    def prepare(self):
        super(NoLoginBase, self).prepare()
        current_user = self.current_user
        if current_user:
            self.redirect(LOGIN_REDIRECT)#%current_user.link)

    def _login(self, user_id, mail, redirect=None):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if not redirect:
            current_user = Zsite.mc_get(user_id)
            redirect = LOGIN_REDIRECT#%current_user.link
        self.redirect(redirect)

@urlmap('/')
class Index(LoginBase):
    def get(self):
        self.render()

@urlmap('/logout')
class Logout(Base):
    def get(self):
        self.clear_cookie('S')
        current_user = self.current_user
        if current_user:
            user_session_rm(current_user.id)
        self.redirect('/')

@urlmap('/login')
class Login(NoLoginBase):
    def get(self):
        self.render(
                errtip = Errtip()
                )
    
    def post(self):
        mail = self.get_argument('mail', None)
        password = self.get_argument('pwd', None)
        print mail,password
        errtip = Errtip()

        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not password:
            errtip.password = '请输入密码'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    return self._login(user_id, mail, self.get_argument('next', None))
                else:
                    errtip.password = '密码有误。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)
            else:
                errtip.mail = """此账号不存在 , <a href="/auth/reg/%s">点此注册</a>"""%escape(mail)

        self.render(
            mail=mail,
            password=password,
            errtip=errtip
        )
