#!/usr/bin/env python
#coding:utf-8
import config
import config.dev

import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
    config.PORT = PORT
else:
    PORT = config.PORT


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
    from zweb.server_cherry import WSGIServer
    from ctrl._application import application
    print 'server on port %s'%PORT
    server = WSGIServer(PORT, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
