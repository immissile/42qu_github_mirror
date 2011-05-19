#!/usr/bin/env python
#coding:utf-8
import config
from zweb.server_tornado import WSGIServer
from god._application import application
import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    port = int(sys.argv[1])
else:
    port = config.GOD_PORT
print 'server on port %s'%port
WSGIServer(port, application)
