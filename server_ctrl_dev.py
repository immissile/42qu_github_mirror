#!/usr/bin/env python
#coding:utf-8
import config
import config.dev
import logging
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

#################

def run():
    from zweb.server_cherry import WSGIServer
    from ctrl._application import application

    from config import SITE_DOMAIN
    print "\nhttp://%s"%SITE_DOMAIN
    print 'SERVE ON PORT %s'%PORT

    server = WSGIServer(PORT, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()





if __name__ == '__main__':

    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
