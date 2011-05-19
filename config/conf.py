#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join, normpath
import sys

#初始化python的查找路径
PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path


PORT = 5555
GOD_PORT = PORT + 11
DEBUG = False


SITE_DOMAIN = '42qu.me'
PIC_URL = 'http://p.42qu.info'
STATIC_URL = 'http://s.42qu.info'
FS_PATH = '/mnt/zpage'


MEMCACHED_ADDR = ('127.0.0.1:11213', )
DISABLE_LOCAL_CACHED = False


MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'zpage'
MYSQL_PASSWD = '42qu.com'
MYSQL_MAIN = 'zpage_main'
