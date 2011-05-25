#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import getpass

CONF_LOCAL = [
    'host_%s' % socket.gethostname(),
    'conf_%s' % getpass.getuser()
]
