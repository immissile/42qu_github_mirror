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
PIC_PATH = '/mnt/zpage'


SMTP = "127.0.0.1"
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
SENDER_MAIL = "test@test.com"


MEMCACHED_ADDR = ('127.0.0.1:11213', )
DISABLE_LOCAL_CACHED = False

MQ_PORT = 14712
MQ_USE = "zsite"

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '12345'
MYSQL_MAIN = 'database_name'

#SMTP = "smtp.sina.com.cn"
#SMTP_USERNAME = "zuroc"
#SMTP_PASSWORD = "kanrss"
#SENDER_MAIL = "zuroc586@sina.com"

LOCAL = locals()

def load(setting):
    print "LOADING SETTING FILE : %s.py"%setting
    try:
        mod = __import__(setting, globals(), locals(), [], -1)
    except ImportError, e:
        print "NO SETTING FILE : %s.py"%setting
    else:
        for i in dir(mod):
            if not i.startswith("__"):
                LOCAL[i] = getattr(mod, i)
import socket
import getpass
for i in (
    'host_%s' % socket.gethostname(),
    'conf_%s' % getpass.getuser()
):
    load(i)

