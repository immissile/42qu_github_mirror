#!/usr/bin/env python
#coding:utf-8


from zkit.errormiddleware import ErrorMiddleware
from config import render
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import sys


def WSGIServer(port, application):
    application = ErrorMiddleware(application, render , "_error.htm")
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

