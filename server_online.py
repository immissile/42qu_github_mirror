#!/usr/bin/env python
#coding:utf-8
import config

from ctrl._application import application

from zkit.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application, config.render ,"_error/500.htm")


import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import sys


def WSGIServer(port, application):
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = config.PORT

    print "server on port %s"%port
    WSGIServer(port, application)
