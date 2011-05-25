#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import getpass

CONF_LOCAL = dict(
    host='host_%s' % socket.gethostname(),
    user='conf_%s' % getpass.getuser()
)

