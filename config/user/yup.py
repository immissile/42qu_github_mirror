

def prepare(o):
    o.SITE_DOMAIN = 'yup.xxx'
    o.PORT = 30300
    o.MYSQL_MAIN = 'zpage'
    o.PIC_DOMAIN = "p.%s"%o.SITE_DOMAIN
    o.FS_DOMAIN = "s.%s"%o.SITE_DOMAIN
    return o

