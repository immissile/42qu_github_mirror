#!/usr/bin/env python
#coding:utf-8


import tornado.web

class Handler(tornado.web.RequestHandler):
    def get_error_html(self, status_code, **kwargs):
        e = kwargs.get('exception')
        if e:
            raise e
        tornado.web.RequestHandler.get_error_html(self, status_code, **kwargs)
