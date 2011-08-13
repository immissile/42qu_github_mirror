def prepare(o):
    o.SITE_DOMAIN = 'zjd.xxx'
    o.PORT = 30200
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FILE_DOMAIN = 'p4.42qu.us'
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    return o
