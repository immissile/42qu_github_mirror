

def prepare(o):
    o.SITE_DOMAIN = 'zuroc.x'
    o.PORT = 2001
    o.MYSQL_MAIN = 'zpage'
    o.PIC_URL = 'http://p.%s'%o.SITE_DOMAIN
    o.FS_URL = 'http://s.%s'%o.SITE_DOMAIN
    return o

