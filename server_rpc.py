#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import tornado.ioloop

def run():
    from rpc._application import application
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = config.RPC_PORT
        if type(port) in (tuple, list):
            port = port[0]
    print 'server on port %s'%str(port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
