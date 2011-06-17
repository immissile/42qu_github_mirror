# -*- coding: utf-8 -*-
from ctrl.main._handler import Base, LoginBase, XsrfGetBase
from cgi import escape
from ctrl._urlmap.auth import urlmap
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from zkit.txt import EMAIL_VALID, mail2link
from zkit.errtip import Errtip

LOGIN_REDIRECT = "%s/live"

@urlmap('/logout')
class Logout(Base):
    def get(self):
        self.clear_cookie('S')
        current_user = self.current_user
        if current_user:
            user_session_rm(current_user.id)
        self.redirect('/')

class NoLoginBase(Base):
    def prepare(self):
        super(NoLoginBase, self).prepare()
        current_user = self.current_user
        if current_user:
            self.redirect(LOGIN_REDIRECT%current_user.link)

@urlmap('/auth/reg/?(.*)')
class Reg(NoLoginBase):
    def get(self, mail=""):
        self.render(
            mail = mail,
            sex = 0,
            password = '',
            errtip = Errtip()
        )

    def post(self, mail=None):
        mail = self.get_argument('mail', '')
        password = self.get_argument('password', '')
        sex = self.get_argument('sex', '0')
        errtip = Errtip()
        if sex:
            sex = int(sex)
            if sex not in (1,2):
                sex = 0

        if not sex:
            errtip.sex = "请选择性别"

        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        if not password:
            errtip.password = '请输入密码'
        
        if not errtip:
            user_id = user_new_by_mail(mail, password)
            return self._login(user_id, mail, '/auth/verify/mail')

        self.render(
            sex=sex, password=password, mail=mail,
            errtip=errtip
        )

@urlmap('/login')
class Login(NoLoginBase):

    def get(self):
        self.render(
            errtip = Errtip()
        )

    def _login(self, user_id, mail, redirect):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if not redirect:
            current_user = Zsite.mc_get(user_id)
            redirect = LOGIN_REDIRECT%current_user.link
        self.redirect(redirect)

    def post(self):
        mail = self.get_argument('mail', None)
        password = self.get_argument('password', None)
        
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
                    errtip.password = '密码有误。忘记密码了？<a href="/password/%s">点此找回</a>' % escape(mail)
            else:
                errtip.mail = """此账号不存在 , <a href="/auth/reg/%s">点此注册</a>"""%escape(mail)

        self.render(
            mail=mail,
            password=password,
            errtip=errtip
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

