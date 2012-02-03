def prepare(o):
               o.SITE_DOMAIN = 'work.xxx'
               o.MYSQL_MAIN = 'zpage'
               o.MYSQL_USER = 'zpage'
               o.MYSQL_PASSWD = '42qu'
               o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
               o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN

