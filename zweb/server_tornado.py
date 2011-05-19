#!/usr/bin/env python
#coding:utf-8
import config.zpage_ctrl
config.zpage_ctrl.DEBUG = False


from zkit.errormiddleware import ErrorMiddleware
from config.zpage_mako import render
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import sys


def WSGIServer(port, application):
    application = ErrorMiddleware(application, render ,"_error/500.htm")
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

