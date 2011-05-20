#!/usr/bin/env python
#coding:utf-8
import config
config.DEBUG = True

from ctrl._application import application

import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
    config.PORT = PORT
else:
    PORT = config.PORT


import tornado.ioloop
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

from cherrypy.wsgiserver import CherryPyWSGIServer

def WSGIServer(port, application):
    from weberror.evalexception import EvalException
    application = EvalException(application, )
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%H:%M:%S',
    )
    def _(environ, start_response):
        logging.info('%s %s'%(environ.get('REQUEST_METHOD'), environ.get('PATH_INFO')))
        return application(environ, start_response)
    return CherryPyWSGIServer(('0.0.0.0', port), _, numthreads=10)


#################
#
#from zkit import static
#from os.path import join
#import re
#
#STATIC_VERSION = re.compile('/\d+?~')
#STATIC_FILE = static.Cling(join(config.PREFIX, 'static'))
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
#                    environ['PATH_INFO'] = STATIC_VERSION.sub('/.', path)
#                return STATIC_FILE(environ, start_response)
#
#        return func(environ, start_response)
#    return _
#
#application = static_middleware(application)
#################

def run():

    print 'server on port %s'%PORT
    server = WSGIServer(PORT, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
