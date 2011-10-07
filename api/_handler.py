# -*- coding: utf-8 -*-
from config import render
import model._db
from zweb._handler import Base as _Base, BaseBase, _login_redirect, login
from model.zsite import Zsite
from model.oauth2 import oauth_access_token_verify
from zweb._handler.main import LoginBase as _LoginBase
from model.user_auth import mail_password_verify


def post(self, *args, **kwds):
    return self.get(*args, **kwds)

class Base(_Base):
    def get(self, *args):
        self.redirect('/')


#class LoginBase(Base):
#    @property
#    def _xsrf(self):
#        return '_xsrf=%s'%self.xsrf_token
#
#    def render(self, template_name=None, **kwds):
#        kwds['_xsrf'] = self._xsrf
#        super(Base, self).render(template_name, **kwds)
#    
#    def prepare(self):
#        super(LoginBase, self).prepare()
#        _login_redirect(self)
#

class LoginBase(_LoginBase):
    post = post

class OauthBase(BaseBase):
    post = post

class OauthAccessBase(OauthBase):
    def prepare(self):
        super(OauthBase, self).prepare()
        if self._finished:
            return
        access_token = self.get_argument('access_token')

        if not access_token:
            self.finish({'error':'miss access_token', 'error_code': 400})
            return

        user_id = oauth_access_token_verify(access_token)

        if not user_id:
            self.finish({'error':'invalid access_token', 'error_code': 401})
            return

        self.current_user_id = user_id

    def get_current_user(self):
        return Zsite.mc_get(self.current_user_id)



class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()


