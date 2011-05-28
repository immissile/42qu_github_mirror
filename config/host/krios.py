def prepare(o):
    o.SITE_DOMAIN = 'work.42qu'
    o.MYSQL_MAIN = 'zpage'
    o.PIC_DOMAIN = "p.%s"%o.SITE_DOMAIN
    o.FS_DOMAIN = "s.%s"%o.SITE_DOMAIN
