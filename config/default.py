#!/usr/bin/env python
# -*- coding: utf-8 -*-


import yajl
import json

json.dump = yajl.dump
json.dumps = yajl.dumps
json.loads = yajl.loads
json.load = yajl.load


import _env
from mysql import DB_MAIN_TABLE, DB_GOOGLE_TABLE
import zkit.cookie_morsel 
from hmako.lookup import TemplateLookup
import sys
from os.path import join
from privilege import PRIVILEGE_IMPORT_FEED



def prepare(o):
    
#    o.REDIS_DB = redis.Redis()

    o.PRIVILEGE_ADMIN = (
        (10014590,(PRIVILEGE_IMPORT_FEED,)), #夭夭
    )

    o.PRIVILEGE_SUPER = set((
        10000000, #张沈鹏 
        10014918, #Zsp 007
        10001542, #010001542
        10001518, #Zsp00 7
        10016605, #Zsp 0 0 7
        10008640, #Z S P007
        10007647, #Z S P 0 0 7
        10030280, #Z S P 00 7
        10030281, #wewt
#        10001299, #真谛~
#        10016494, #周凯华
#        10000212, #张近东
#        10001637, #陶紫旺
    ))

    o.SITE_DOMAIN = '42qu.test'
    o.SITE_NAME = '42区'
    o.PORT = 6666

    o.UPYUN_DOMAIN = '1.42qu.us'
    o.UPYUN_URL = 'http://%s/%%s'%o.UPYUN_DOMAIN

    o.REDIS_CONFIG = {
        "unix_socket_path":"/tmp/redis.sock"
    }
    o.MYSQL_HOST = '127.0.0.1'
    o.MYSQL_PORT = '3306'
    o.MYSQL_MAIN = 'zpage'
    o.MYSQL_USER = 'root'
    o.MYSQL_PASSWD = '42qu'


    o.MQ_PORT = 11300
    o.MQ_FAIL_MAIL_ADDR = "zsp007@gmail.com"

    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN

    o.DEBUG = False

    o.SHORT_DOMAIN = '42qu.us'

    o.DISABLE_LOCAL_CACHED = False
    o.MEMCACHED_ADDR = ('127.0.0.1:11211', )

    o.SMTP = 'smtp.sina.com'
    o.SMTP_USERNAME = '42qutest'
    o.SMTP_PASSWORD = '42qu.com'
    o.SENDER_MAIL = '42qutest@sina.com'

    o.ZSITE_BIND_FOR_SYNC = 10008639

    if not getattr(o, 'ADMIN_MAIL', None):
        o.ADMIN_MAIL = o.SENDER_MAIL
#    o.SMTP = 'smtp.163.com'
#    o.SMTP_USERNAME = 'zpagedev'
#    o.SMTP_PASSWORD = '42qu_com'
#    o.SENDER_MAIL = 'zpagedev@163.com'

    o.LOGO_TEXT = '找到给你答案的人'

    o.ALIPAY_ID = ''
    o.ALIPAY_SALT = ''
    o.ALIPAY_EMAIL = ''

    o.TWITTER_CONSUMER_KEY = ''
    o.TWITTER_CONSUMER_SECRET = ''

    o.WWW163_CONSUMER_KEY = ''
    o.WWW163_CONSUMER_SECRET = ''

    o.SINA_CONSUMER_KEY = ''
    o.SINA_CONSUMER_SECRET = ''

    o.SOHU_CONSUMER_KEY = ''
    o.SOHU_CONSUMER_SECRET = ''

    o.QQ_CONSUMER_KEY = ''
    o.QQ_CONSUMER_SECRET = ''

    o.RENREN_CONSUMER_KEY = ''
    o.RENREN_CONSUMER_SECRET = ''

    o.GOOGLE_CONSUMER_REAL_SECRET = ''
    o.GOOGLE_CONSUMER_SECRET = ''

    o.DOUBAN_CONSUMER_KEY = ''
    o.DOUBAN_CONSUMER_SECRET = ''

    o.GOD_PORT = None
    o.RPC_PORT = None
    o.API_PORT = None

    o.SINA_FOLLOW = '1827906323'
    o.WWW163_FOLLOW = '6122584690'
    o.QQ_FOLLOW = 'cn42qu'
    o.RENREN_FOLLOW = ''

    o.GREADER_PASSWORD = ''
    o.GREADER_USERNAME = ''

    

    return o


def debug(o):
    o.DEBUG = True


def finish(o):
    MYSQL_MAIN = o.MYSQL_MAIN

    o.MQ_USE = MYSQL_MAIN

    o.FILE_PATH = '/mnt/%s'%MYSQL_MAIN
    o.SEARCH_DB_PATH = '/mnt/%s_searchdb'%MYSQL_MAIN


    if not o.GOD_PORT:
        o.GOD_PORT = o.PORT + 20

    if not o.API_PORT:
        o.API_PORT = o.PORT + 30

    if not o.RPC_PORT:
        o.RPC_PORT = o.PORT + 40


    o.FILE_URL = 'http://%s'%o.FILE_DOMAIN
    o.FS_URL = 'http://%s'%o.FS_DOMAIN

    o.SITE_DOMAIN_SUFFIX = '.%s' % o.SITE_DOMAIN
    o.SITE_URL = '//%s' % o.SITE_DOMAIN
    o.SITE_HTTP = 'http://%s' % o.SITE_DOMAIN

    o.API_URL = '//api.%s' % o.SITE_DOMAIN
    o.API_HTTP = 'http:%s' % o.API_URL
    o.RPC_URL = '//RPC.%s' % o.SITE_DOMAIN
    o.RPC_HTTP = 'http:%s' % o.RPC_URL

    o.DUMPLICATE_DB_PREFIX = '%s/%s.dumplicate.%%s.kch'%(o.FILE_PATH , o.SITE_DOMAIN)
    o.SENDER_NAME = o.SITE_DOMAIN

    HTM_PATH = join(_env.PREFIX, 'htm')
    MAKOLOOKUP = TemplateLookup(
        directories=HTM_PATH,
        module_directory='/tmp/%s'%HTM_PATH.strip('/').replace('/', '.'),
        disable_unicode=True,
        encoding_errors='ignore',
        default_filters=['str', 'h'],
        filesystem_checks=o.DEBUG,
        input_encoding='utf-8',
        output_encoding=''
    )


    def render(htm, **kwds):
        mytemplate = MAKOLOOKUP.get_template(htm)
        return mytemplate.render(**kwds)
    o.render = render

    DB_HOST_MAIN = '%s:%s:%s:%s:%s' % (
        o.MYSQL_HOST, o.MYSQL_PORT, o.MYSQL_MAIN, o.MYSQL_USER, o.MYSQL_PASSWD
    )
    DB_HOST_GOOGLE = '%s:%s:%s:%s:%s' % (
        o.MYSQL_HOST, o.MYSQL_PORT, '%s_google'%o.MYSQL_MAIN, o.MYSQL_USER, o.MYSQL_PASSWD
    )


    o.DB_CONFIG = {
        'main': {
            'master': DB_HOST_MAIN,
            'tables': DB_MAIN_TABLE,
        },
        'google': {
            'master': DB_HOST_GOOGLE,
            'tables': DB_GOOGLE_TABLE,
        },
    }
    return o

def load(self, *args):
    PREPARE = [
        prepare
    ]
    FINISH = [
        finish
    ]

    def load(name):
        try:
            mod = __import__(
                name,
                globals(),
                locals(),
                [],
                -1
            )
        except ImportError:
            print 'NO CONFIG %s'%name
            return
        for i in name.split('.')[1:]:
            mod = getattr(mod, i)
        prepare = getattr(mod, 'prepare', None)

        if prepare:
            PREPARE.append(prepare)

        finish = getattr(mod, 'finish', None)
        if finish:
            FINISH.append(finish)
    for i in args:
        load(i)
    funclist = PREPARE+list(reversed(FINISH))
    for _ in funclist:
        _(self)

    return self
