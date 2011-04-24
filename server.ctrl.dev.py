#!/usr/bin/env python
#coding:utf-8
import config.zpage_ctrl
config.zpage_ctrl.DEBUG = True

from ctrl._application import application
from weberror.evalexception import EvalException
application = EvalException(application, )


import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

from zkit.wsgiserver import CherryPyWSGIServer

def WSGIServer(port, application):
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d]  %(message)s',
        datefmt='%H:%M:%S',
    )
    def _(environ, start_response):
        logging.info("%s %s"%(environ.get('REQUEST_METHOD'), environ.get('PATH_INFO')))
        return application(environ, start_response)
    return CherryPyWSGIServer(('0.0.0.0', port), _, numthreads=1)

def run():
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

if __name__ == "__main__":
    from zkit.reloader.reload_server import auto_reload
    while True:
        auto_reload(run)
        print "\nSleep 4 seconds"
        for i in xrange(10, 0, -1):
            sleep(0.4)
            print i,
        print ""
