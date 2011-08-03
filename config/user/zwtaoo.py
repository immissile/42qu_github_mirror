def prepare(o):
    o.SITE_DOMAIN = 'zwtaoo.xxx'
    o.PORT = 30400
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    return o
