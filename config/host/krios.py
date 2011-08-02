def prepare(o):
    o.SITE_DOMAIN = 'work.xxx'
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    import _private
    _private.prepare(o)
