#!/usr/bin/env python
#coding:utf-8
import sys
import tornado.httpserver
import tornado.ioloop
from tornado.wsgi import WSGIContainer
from zkit.errormiddleware import ErrorMiddleware
from config import render


def WSGIServer(port, application):
    application = ErrorMiddleware(application, render, '_error.htm')
    container = WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
