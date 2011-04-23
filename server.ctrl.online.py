#!/usr/bin/env python
#coding:utf-8
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop


def WSGIServer(port, application):
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    from ctrl._application import application
    import config.zpage_ctrl
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = config.zpage_ctrl.PORT

    print "server on port %s"%port
    WSGIServer(port, application)

