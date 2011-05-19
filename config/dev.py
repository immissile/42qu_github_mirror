#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf

conf.DEBUG = True
conf.SITE_DOMAIN = "42qu.info"

import getpass
LOCAL_SETTINGS = 'dev_%s' % getpass.getuser()
try:
    __import__(LOCAL_SETTINGS, globals(), locals(), [], -1)
except ImportError, e:
    print e
