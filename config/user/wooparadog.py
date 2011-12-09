def prepare(o):
    o.SITE_DOMAIN = 'wooparadog.xxx'
    o.PORT = 30900
    o.MQ_PORT = 11500
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    return o
