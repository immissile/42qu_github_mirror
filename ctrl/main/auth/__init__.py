# -*- coding: utf-8 -*-
from ctrl.main._handler import Base, LoginBase, XsrfGetBase
from cgi import escape
from ctrl._urlmap.auth import urlmap
from model.cid import CID_VERIFY_MAIL, CID_VERIFY_PASSWORD
from model.namecard import namecard_get, namecard_new
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.user_mail import mail_by_user_id, user_id_by_mail
from model.user_session import user_session, user_session_rm
from model.verify import verify_mail_new, verifyed
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE
from zkit.txt import EMAIL_VALID, mail2link
from zkit.errtip import Errtip
from model.user_new import user_new
from model.oauth import oauth_token_key_by_id, token_key_login_set
from config import SITE_URL
from model.sync import sync_follow_new

LOGIN_REDIRECT = '%s/feed'

@urlmap('/logout')
class Logout(XsrfGetBase):
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

    def _login(self, user_id, mail, redirect=None):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if not redirect:
            current_user = Zsite.mc_get(user_id)
            redirect = LOGIN_REDIRECT%current_user.link
        self.redirect(redirect)




@urlmap('/auth/reg/?(.*)')
class Reg(NoLoginBase):
    def get(self, mail=''):
        self.render(
            mail=mail,
            sex=0,
            errtip=Errtip(),
        )

    def post(self, mail=None):
        mail = self.get_argument('mail', '')
        sex = self.get_argument('sex', '0')
        errtip = Errtip()
        if sex:
            sex = int(sex)
            if sex not in (1, 2):
                sex = 0

        if mail:
            mail = mail.lower()
        if not mail:
            errtip.mail = '请输入邮箱'
        elif not EMAIL_VALID.match(mail):
            errtip.mail = '邮箱格式有误'

        #if not password:
        #    errtip.password = '请输入密码'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                #if user_password_verify(user_id, password):
                #    return self._login(user_id, mail)
                #else:
                errtip.mail = '邮箱已注册。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)

        if not sex:
            errtip.sex = '请选择性别'

        if not errtip:
            user_id = user_new(mail, sex=sex)
            return self.redirect('/auth/verify/send/%s'%user_id)

        self.render(
            sex=sex,
            mail=mail,
            errtip=errtip
        )


@urlmap('/login')
class Login(NoLoginBase):
    def get(self):
        if self.get_cookie('E'):
            url = '/auth/login'
        else:
            url = '/auth/reg'
        self.redirect(url)


def _mail_password_post(self):
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

    user_id = 0
    if not errtip:
        user_id = user_id_by_mail(mail)
        if user_id:
            if not user_password_verify(user_id, password):
                errtip.password = '密码有误。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)

    return user_id , mail, password, errtip

@urlmap('/auth/login')
class AuthLogin(NoLoginBase):

    def get(self):
        self.render(
            errtip=Errtip()
        )

    _mail_password_post = _mail_password_post

    def post(self):
        user_id, mail, password, errtip = self._mail_password_post()
        if not errtip:
            if user_id:
                return self._login(user_id, mail, self.get_argument('next', None))
            else:
                errtip.mail = """此账号不存在 , <a href="/auth/reg/%s">点此注册</a>"""%escape(mail)

        self.render(
            mail=mail,
            password=password,
            errtip=errtip
        )


@urlmap('/auth/bind/(\d+)')
class AuthBind(NoLoginBase):
    def _prepare(self, id):
        key = self.get_argument('key', None)

        cid, token_user_id, _key = oauth_token_key_by_id(id)
        self.token_user_id = token_user_id
        self.cid = cid
        if not key or key != _key:
            return self.redirect('/')

    def get(self, id):
        self._prepare(id)
        errtip = Errtip()
        self.render(errtip=errtip)

    def post(self, id):
        self._prepare(id)
        errtip = Errtip()
        user_id, mail, password, errtip = self._mail_password_post()

        if not errtip:

            if user_id:
                token_key_login_set(id, user_id)
                return self._login(user_id, mail, self.get_argument('next', None))
            else:
                token_key_login_set(id, user_id)
                user_id = user_new(mail, password=password)

                sync_txt = self.get_argument('sync_txt', None)
                txt = self.get_argument('weibo', None)
                flag = 0
                if sync_txt:
                    flag |= 0b10

                sync_follow_new(user_id, flag, self.cid, txt, id)

                return self.redirect('/auth/verify/send/%s'%user_id)

        self.render(errtip=errtip)

    _mail_password_post = _mail_password_post

