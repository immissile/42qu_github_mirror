#coding:utf-8

import getpass
from socket import gethostname

def prepare(o):
    o.SITE_DOMAIN = '%s%s.tk'%(getpass.getuser(),gethostname()) 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN

    o.MYSQL_USER = 'zpage'
    o.MYSQL_PASSWD = '42qudev'

    try:
        import _private
    except ImportError:
        pass
    else:
        _private.prepare(o)

