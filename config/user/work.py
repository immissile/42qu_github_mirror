def prepare(o):
    o.SITE_DOMAIN = 'work.xxx'
    o.PORT = 30000
    o.PIC_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    return o
