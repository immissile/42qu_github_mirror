#!/usr/bin/env python
#coding:utf-8
import config.dev
import config.zpage_ctrl
config.zpage_ctrl.DEBUG = True

import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
    config.zpage_ctrl.PORT = PORT
else:
    PORT = config.zpage_ctrl.PORT


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
        format='%(asctime)s %(message)s',
        datefmt='%H:%M:%S',
    )
    def _(environ, start_response):
        logging.info("%s %s"%(environ.get('REQUEST_METHOD'), environ.get('PATH_INFO')))
        return application(environ, start_response)
    return CherryPyWSGIServer(('0.0.0.0', port), _, numthreads=10)


#################
#
#from zkit import static
#from os.path import join
#import re
#
#STATIC_VERSION = re.compile("/\d+?~")
#STATIC_FILE = static.Cling(join(config.zpage_ctrl.PREFIX, "static"))
#STATIC_PATH = ('/css/', '/js/', '/pic/', '/img/', '/favicon.ico', '/bazs.cert', '/robots.txt')
#
#def static_middleware(func):
#    def _(environ, start_response):
#        path = environ['PATH_INFO']
#
#        #print environ
#        for i in STATIC_PATH:
#            if path.startswith(i):
#                if i in ('/css/', '/js/'):
#                    environ['PATH_INFO'] = STATIC_VERSION.sub("/.", path)
#                return STATIC_FILE(environ, start_response)
#
#        return func(environ, start_response)
#    return _
#
#application = static_middleware(application)
#################

def run():

    print "server on port %s"%PORT
    server = WSGIServer(PORT, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    from zkit.reloader.reload_server import auto_reload
    from time import sleep
    while True:
        auto_reload(run)
        print "\nSleep 4 seconds"
        for i in xrange(10, 0, -1):
            sleep(0.4)
            print i,
        print ""
