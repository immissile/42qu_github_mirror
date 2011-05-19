#!/usr/bin/env python
#coding:utf-8

from zweb._tornado import web
from config import render
from model.user_session import user_id_by_session
from model.zsite import Zsite
from sqlbean.metamodel import lower_name

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


    def render(self, template_name=None, **kwds):
        if template_name is None:
            if not hasattr(self, "template"):
                self.template = "%s/%s.htm"%(
                    self.__module__.replace(".", "/"),
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



