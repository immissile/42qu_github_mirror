def prepare(o):
    o.SITE_DOMAIN = 'work.xxx'
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    try:
        import _private
    except ImportError:
        pass
    else:
        _private.prepare(o)

