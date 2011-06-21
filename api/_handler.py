# -*- coding: utf-8 -*-
from config import render
import model._db
from model.api_client import api_sign_verify, api_login_verify
from model.api_error import API_ERROR_SIGN, API_ERROR_LOGIN
from zweb._handler import Base as _Base, BaseBase, _login_redirect, login
from model.zsite import Zsite

def post(self, *args, **kwds):
    return self.get(*args, **kwds)

class Base(_Base):
    def get(self, *args):
        self.redirect('/')

    @property
    def _xsrf(self):
        return '_xsrf=%s'%self.xsrf_token

    def render(self, template_name=None, **kwds):
        kwds['_xsrf'] = self._xsrf
        super(Base, self).render(template_name, **kwds)

    post = post

class LoginBase(Base):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)

class ApiBase(BaseBase):
    post = post

class ApiSignBase(ApiBase):
    def prepare(self):
        arguments = self.request.arguments
        arguments = dict([
            (k, v[0]) for k, v in arguments.iteritems()
        ])
        if api_sign_verify(arguments):
            super(ApiBase, self).prepare()
        else:
            self.finish(API_ERROR_SIGN)

class ApiLoginBase(ApiSignBase):
    def prepare(self):
        super(ApiBase, self).prepare()
        if self._finished:
            return
        S = self.get_argument("S")
        client_id = self.get_argument('client_id')
        user_id = api_login_verify(client_id, S)
        if not user_id:
            self.finish(API_ERROR_LOGIN)
        self.current_user_id = user_id

    def get_current_user(self):
        return Zsite.mc_get(self.current_user_id)

