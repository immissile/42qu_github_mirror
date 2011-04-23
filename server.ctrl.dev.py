#!/usr/bin/env python
#coding:utf-8
import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

from zkit.wsgiserver import CherryPyWSGIServer 

def WSGIServer(port, application):
    return CherryPyWSGIServer(('0.0.0.0',port),application)

if __name__ == "__main__":
    from ctrl._application import application
    import config.zpage_ctrl
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = config.zpage_ctrl.PORT

    print "server on port %s"%port
    server = WSGIServer(port, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
