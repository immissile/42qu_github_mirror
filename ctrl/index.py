#!/usr/bin/env python
#coding:utf-8


import tornado.web
from _urlmap import urlmap


@urlmap("/")
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world2")


