#!/usr/bin/env python
#coding:utf-8

from _tornado import web
from config.zpage_mako import render
from config import SITE_DOMAIN, SITE_URL
from config import PORT
from model.zsite_link import zsite_by_domain
from model.user_session import user_id_by_session
from model.zsite import Zsite
import urlparse
import urllib

def lower_name(class_name):
    """
>>>lower_name("UserCount")
    'user_count'

>>>lower_name("user_count")
    'user_count'
    """
    result = []
    for c in class_name:
        i = ord(c)
        if 65 <= i <= 90:
            if result:
                if not 48 <= ord(result[-1]) <= 57:
                    result.append("_")
            i += 32
            c = chr(i)
        result.append(c)
    return "".join(result)


class Base(web.RequestHandler):
    def get_current_user(self):
        key = "S"
        session = self.get_cookie(key)
        if session:
            user_id = user_id_by_session(session)
            if user_id:
                user = Zsite.get(user_id)
                return user
            else:
                self.clear_cookie(key)

#    def get_error_html(self, status_code, **kwargs):
#        e = kwargs.get('exception')
#        if e:
#            raise e
#        web.RequestHandler.get_error_html(self, status_code, **kwargs)


    def render(self, template_name=None, **kwds):
        if template_name is None:
            if not hasattr(self, "template"):
                self.template = "%s/%s.htm"%(
                    self.__module__.split(".", 1)[1],
                    lower_name(self.__class__.__name__)
                )
            template_name = self.template
        current_user = self.current_user
        kwds['current_user'] = current_user
        kwds['request'] = self.request
        kwds['xsrf_form_html'] = self.xsrf_form_html
        kwds['zsite'] = self.zsite
        if not self._finished:
            self.finish(render(template_name, **kwds))


    def prepare(self):
        host = self.request.host
        zsite = zsite_by_domain(host)
        self.zsite = zsite
        if zsite is None and not host.startswith(SITE_DOMAIN):
            return self.redirect(SITE_URL)


class LoginBase(Base):
    def prepare(self):
        if not self.current_user:
            url = self.get_login_url()
            if "?" not in url:
                if urlparse.urlsplit(url).scheme:
                    # if login url is absolute, make next absolute too
                    next_url = self.request.full_url()
                else:
                    next_url = self.request.uri
                url += "?" + urllib.urlencode(dict(next=next_url))
            self.redirect(url)
            return
        super(LoginBase,self).prepare()


