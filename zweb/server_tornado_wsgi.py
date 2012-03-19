#!/usr/bin/env python
#coding:utf-8
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



class Run(object):
    def __init__(self, port, application, wsgi_server=WSGIServer):
        self.port = port
        self.application = application
        self.wsgi_server = wsgi_server

    def __call__(self):
        import sys
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            port = int(sys.argv[1])
        else:
            port = self.port
            if type(port) in (list, tuple):
                port = port[0]

        print 'server on port %s'%port

        self.wsgi_server(port, self.application)


