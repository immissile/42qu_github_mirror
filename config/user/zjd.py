

def prepare(o):
    o.SITE_DOMAIN = 'zjd.42qu'
    o.PORT = 30200
    o.MYSQL_MAIN = 'zpage'
    o.PIC_DOMAIN = "p.%s"%o.SITE_DOMAIN
    o.FS_DOMAIN = "s.%s"%o.SITE_DOMAIN
    return o

