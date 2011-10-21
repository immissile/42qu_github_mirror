def prepare(o):
    o.SITE_DOMAIN = 'yup.xxx'
    o.PORT = 30300
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.RENREN_CUNSUMER_KEY = 'e7f7a7eea0d943a5b3dcfa17a5574ecc'
    o.RENREN_CUNSUMER_SECRET = '649b18e9f131424e9b75488112098068'
    return o
