#!/usr/bin/env python
#coding:utf-8


import tornado.web
import _url

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


