#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import urllib
import urlparse
from zsql.metamodel import lower_name
from zweb._tornado import web
from config import render, SITE_DOMAIN, SITE_URL
from model._db import mc
from model.user_session import user_id_by_session
from model.zsite import Zsite
from static import css, js


RENDER_KWDS = {
    'css':css,
    'js':js
}

class BaseBase(web.RequestHandler):
    def decode_argument(self, value, name=None):
        return value

    def prepare(self):
        mc.reset()
        super(BaseBase, self).prepare()

#    def redirect(self, url, permanent=False):
#        if self._finished:
#            return
#        super(BaseBase,self).redirect(url, permanent)

class Base(BaseBase):
    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            current_user = self.current_user
            if current_user:
                self._current_user_id = current_user.id
            else:
                self._current_user_id = 0
        return self._current_user_id

    def render(self, template_name=None, **kwds):
        if template_name is None:
            if not hasattr(self, 'template'):
                self.template = '%s/%s.htm' % (
                    self.__module__.replace('.', '/'),
                    lower_name(self.__class__.__name__)
                )
            template_name = self.template

        current_user = self.current_user
        kwds['current_user'] = current_user
        kwds['current_user_id'] = self.current_user_id
        kwds['request'] = self.request
        kwds['this'] = self
        kwds.update(RENDER_KWDS)
        if not self._finished:
            self.finish(render(template_name, **kwds))

    def get_current_user(self):
        key = 'S'
        session = self.get_cookie(key)
        if session:
            user_id = user_id_by_session(session)
            if user_id:
                user = Zsite.mc_get(user_id)
                return user
            else:
                self.clear_cookie(key)



def _login_redirect(self):
    if self._finished:
        return
    if not self.current_user:
        url = self.get_login_url()
        if '?' not in url:
            if urlparse.urlsplit(url).scheme:
                # if login url is absolute, make next absolute too
                next_url = self.request.full_url()
            else:
                next_url = self.request.uri
            request = self.request
            host = request.host
            if host != SITE_DOMAIN and next_url.startswith('/') and not next_url.startswith('//'):
                next_url = '//%s%s'%(host, next_url)
            url += '?' + urllib.urlencode(dict(next=next_url))
        self.clear_cookie('S')
        self.redirect(url)
        return True


def login(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if _login_redirect(self):
            return
        return method(self, *args, **kwargs)
    return wrapper
