#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf
from conf import load

import socket
load('host_dev_%s' % socket.gethostname())

import getpass
load('conf_dev_%s' % getpass.getuser())

conf.DEBUG = True
