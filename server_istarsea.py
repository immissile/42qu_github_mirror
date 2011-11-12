#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
from zweb.server_tornado import WSGIServer
from ctrl._istarsea import application
import sys
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    port = int(sys.argv[1])
else:
    port = config.PORT
    if type(port) in (list, tuple):
        port = port[0]

print 'server on port %s'%port
WSGIServer(port, application)
