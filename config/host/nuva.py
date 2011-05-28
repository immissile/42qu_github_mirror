def prepare(o):
    o.SITE_DOMAIN = '42qu.me'
    o.PIC_DOMAIN = "p.%s"%o.SITE_DOMAIN
    o.FS_DOMAIN = "s.%s"%o.SITE_DOMAIN
    o.MYSQL_MAIN = 'zpage_main'
    o.MYSQL_USER = "zpage"
    o.MYSQL_PASSWD = "42qu.com"
    o.MYSQL_HOST = "127.0.0.1"
    o.MYSQL_PORT = "3306"
