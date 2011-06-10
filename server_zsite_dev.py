#!/usr/bin/env python
#coding:utf-8
import config
import config.dev

import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])
else:
    PORT = config.ZSITE_PORT

def run():
    from zweb.server_cherry import WSGIServer
    from zsite._application import application
    print 'server on port %s'%PORT
    server = WSGIServer(PORT, application)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
