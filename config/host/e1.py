#coding:utf-8

import getpass

def prepare(o):
    o.SITE_DOMAIN = '%squ.tk'%getpass.getuser()
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

