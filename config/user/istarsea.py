def prepare(o):
    o.SITE_DOMAIN = SITE_DOMAIN = 'istarsea.com'
    FILE_DOMAIN = 'istarsea.co'
    o.PORT = 30100
    o.MYSQL_MAIN = 'istarsea'
    o.FILE_DOMAIN = 'p.%s'%FILE_DOMAIN
    o.FS_DOMAIN = 's.%s'%FILE_DOMAIN
    o.MYSQL_USER = 'istarsea'
    o.MYSQL_PASSWD = 'upuQDqvXGBfQz4QR'
    o.MYSQL_PORT = '13307'
    o.MEMCACHED_ADDR = ('127.0.0.1:11509', )
    o.SMTP = '127.0.0.1'
    o.SMTP_USERNAME = ''
    o.SMTP_PASSWORD = ''
    o.SENDER_MAIL = 'i@%s'%SITE_DOMAIN
    o.ADMIN_MAIL = 'xning@%s'%SITE_DOMAIN

    o.PORT = (
        40050,
        40051,
        40052,
        40053,
    )

    o.GOD_PORT = (
        40021,
        40023,
    )

    o.API_PORT = (
        40060,
        40061,
    )

    o.RPC_PORT = (
        40070,
        40071,
    )

    o.M_PORT = (
        40080,
        40081,
    )

    return o

