#!/usr/bin/env python
#coding:utf-8


import tornado.web
from config.zpage_mako import render



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


class Base(tornado.web.RequestHandler):
    def get_error_html(self, status_code, **kwargs):
        e = kwargs.get('exception')
        if e:
            raise e
        tornado.web.RequestHandler.get_error_html(self, status_code, **kwargs)


    def render(self, template_name=None, **kwds):
        if template_name is None:
            if not hasattr(self, "template"):
                self.template = "%s/%s.htm"%(
                    self.__module__.split(".",1)[1],
                    lower_name(self.__class__.__name__)
                )
            template_name = self.template
        self.finish(render(template_name, **kwds))
