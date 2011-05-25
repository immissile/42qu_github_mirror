#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import getpass

for i in (
    'host_%s' % socket.gethostname(),
    'conf_%s' % getpass.getuser()
):
    load(i)
print "load conf"




