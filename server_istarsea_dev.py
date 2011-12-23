#!/usr/bin/env python
#coding:utf-8
import config
import config.dev
import logging
import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    port = int(sys.argv[1])
    config.PORT = port
else:
    port = config.PORT
    if type(port) in (list, tuple):
        port = port[0]


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

#################

def run():
    from zweb.server_cherry import WSGIServer
    from ctrl._istarsea import application

    from config import SITE_DOMAIN
    print '\nhttp://%s'%SITE_DOMAIN
    print 'SERVE ON PORT %s'%port

    server = WSGIServer(port, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()





if __name__ == '__main__':

    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
