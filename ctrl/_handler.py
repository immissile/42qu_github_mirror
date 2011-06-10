#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import render
from zweb._handler import Base as _Base, _login_redirect, login

class Base(_Base):
    def get(self):
        self.redirect('/')

    @property
    def _xsrf(self):
        return '_xsrf=%s'%self.xsrf_token

    def render(self, template_name=None, **kwds):
        kwds['_xsrf'] = self._xsrf
        super(Base, self).render(template_name, **kwds)

class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish('{"login":1}')

class LoginBase(Base):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)

class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()
