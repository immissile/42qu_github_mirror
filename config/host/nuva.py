# -*- coding: utf-8 -*-

def prepare(o):
    o.SITE_DOMAIN = '42qu.me'
    o.PIC_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.MYSQL_MAIN = 'zpage_main'
    o.MYSQL_USER = 'zpage'
    o.MYSQL_PASSWD = '42qu.com'
    o.MYSQL_HOST = '127.0.0.1'
    o.MYSQL_PORT = '3306'
    o.MQ_PORT = 14712
    o.MEMCACHED_ADDR = ('127.0.0.1:11508', )
    o.SMTP = '127.0.0.1'
    o.SMTP_USERNAME = ''
    o.SMTP_PASSWORD = ''
    o.SENDER_MAIL = '42qu@42qu.com'

    o.ALIPAY_SALT = 'ri3woiadltar53f4snayzf78mhpmfgtf'
    o.ALIPAY_ID = '2088002484028020'
    o.ALIPAY_EMAIL = 'zsp007@gmail.com'
