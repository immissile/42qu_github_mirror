# -*- coding: utf-8 -*-
from _handler import Base as BaseBase, LoginBase, XsrfGetBase
from ctrl._urlmap.main import urlmap
from config import SITE_DOMAIN
from zkit.errtip import Errtip
from zkit.txt import EMAIL_VALID, mail2link
from model.oauth import oauth_token_by_oauth_id
from model.user_mail import mail_by_user_id, user_id_by_mail
from cgi import escape
from model.user_auth import user_password_new, user_password_verify, user_new_by_mail
from model.oauth import oauth_zsite_id_update_by_oauth_id
from model.user_session import user_session, user_session_rm
from model.zsite import Zsite
LOGIN_REDIRECT = '%s/live'


class Base(BaseBase):
    def _login(self, user_id, mail, redirect=None):
        session = user_session(user_id)
        self.set_cookie('S', session)
        self.set_cookie('E', mail)
        if not redirect:
            current_user = Zsite.mc_get(user_id)
            redirect = LOGIN_REDIRECT%current_user.link
        self.redirect(redirect)


@urlmap('/bind/login')
class BindLogin(Base):
    def get(self):
        oauth_id = self.get_argument('id',None)
        oauth_key = self.get_argument('key',None)
        email = self.get_cookie('E',None)
        if not (oauth_key and oauth_id):
            self.redirect(SITE_DOMAIN)
        im =  oauth_token_by_oauth_id(oauth_id)
        if im and im.zsite_id:
            if im.token_key == oauth_key:
                user_mail = mail_by_user_id(im.zsite_id)
                self._login(im.zsite_id,user_mail)
        
            if oauth_key != im.token_key:
                errtip.oauth_key = '请求非法'

        self.render(email = email,
                errtip = Errtip(),
                oauth_key = oauth_key,
                oauth_id = oauth_id
                )
    def post(self):
        mail = self.get_argument('mail', None)
        oauth_id = self.get_argument('oauth_id', None)
        oauth_key = self.get_argument('oauth_key', None)
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
        
        if not (oauth_id and oauth_key):
            errtip.oauth_id = '请求非法'
        
        im =  oauth_token_by_oauth_id(oauth_id)
        if im:
            if oauth_key != im.token_key:
                errtip.oauth_key = '请求非法'
        
        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    
                    oauth_zsite_id_update_by_oauth_id(oauth_id,user_id)
                    self._login(user_id,mail,self.get_argument('next',None))
                else:
                    errtip.password = '密码有误。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)
            else:
                errtip.mail = """此账号不存在 , <a href="/auth/reg/%s">点此注册</a>"""%escape(mail)

        self.render(
            mail=mail,
            password=password,
            errtip=errtip,
            oauth_key = oauth_key,
            oauth_id = oauth_id
        )


@urlmap('/bind/reg')
class BindReg(Base):
    def get(self):
        oauth_id = self.get_argument('id',None)
        oauth_key = self.get_argument('key',None)
        if not (oauth_key and oauth_id):
            self.redirect(SITE_DOMAIN)
        self.render(
            oauth_key=oauth_key,
            oauth_id=oauth_id,
            mail='',
            sex=0,
            password='',
            errtip=Errtip(),
            zsite_list='',
        )
    def post(self, mail=None):
        oauth_id = self.get_argument('oauth_id', None)
        oauth_key = self.get_argument('oauth_key', None)
        mail = self.get_argument('mail', '')
        password = self.get_argument('password', '')
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

        if not password:
            errtip.password = '请输入密码'
        
        if not (oauth_id and oauth_key):
            errtip.oauth_id = '请求非法'
        
        im =  oauth_token_by_oauth_id(oauth_id)
        if im:
            if oauth_key != im.token_key:
                errtip.oauth_key = '请求非法'

        if not errtip:
            user_id = user_id_by_mail(mail)
            if user_id:
                if user_password_verify(user_id, password):
                    oauth_zsite_id_update_by_oauth_id(oauth_id,user_id)
                    return self._login(user_id, mail)
                else:
                    errtip.password = '邮箱已注册。忘记密码了？<a href="/auth/password/reset/%s">点此找回</a>' % escape(mail)

        if not sex:
            errtip.sex = '请选择性别'

        if not errtip:
            user = user_new_by_mail(mail, password)
            user_id = user.id
            user_info_new(user_id, sex=sex)
            search_new(user_id)
            oauth_zsite_id_update_by_oauth_id(oauth_id,user_id)
            return self.redirect('/auth/verify/send/%s'%user_id)

        self.render(
            sex=sex, password=password, mail=mail,
            errtip=errtip
        )
