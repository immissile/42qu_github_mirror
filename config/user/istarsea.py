def prepare(o):
    o.SITE_DOMAIN = 'istarsea.com'
    FILE_DOMAIN = "istarsea.co"
    o.PORT = 30100
    o.MYSQL_MAIN = 'istarsea'
    o.FILE_DOMAIN = 'p.%s'%FILE_DOMAIN
    o.FS_DOMAIN = 's.%s'%FILE_DOMAIN
    o.MYSQL_USER = 'istarsea'
    o.MYSQL_PASSWD = 'upuQDqvXGBfQz4QR'
    o.MYSQL_PORT = '13307'
    return o
