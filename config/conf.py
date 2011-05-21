#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join, normpath
import sys

#初始化python的查找路径
PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path


PORT = 5555
DEBUG = False


SITE_DOMAIN = '42qu.me'
PIC_URL = 'http://p.42qu.info'
FS_URL = 'http://s.42qu.info'
FS_PATH = '/mnt/zpage'


MEMCACHED_ADDR = ('127.0.0.1:11213', )
DISABLE_LOCAL_CACHED = False

MQ_PORT = 14712
MQ_USE = "zsite"

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'zpage'
MYSQL_PASSWD = '42qu.com'
MYSQL_MAIN = 'zpage_main'

#SMTP = "smtp.sina.com.cn"
#SMTP_USERNAME = "zuroc"
#SMTP_PASSWORD = "kanrss"
#SYS_EMAIL_SENDER = "zuroc586@sina.com"

def load(setting):
    try:
        __import__(setting, globals(), locals(), [], -1)
    except ImportError, e:
        print "NO SETTING FILE : %s.py"%setting

import socket
load("host_%s"%socket.gethostname())

import getpass
load('conf_%s' % getpass.getuser())
