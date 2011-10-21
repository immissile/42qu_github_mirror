def prepare(o):
    o.SITE_DOMAIN = 'yup.xxx'
    o.PORT = 30300
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.GOOGLE_CONSUMER_KEY = '518129477934.apps.googleusercontent.com'
    o.GOOGLE_CONSUMER_SECRET = 'FRWbGhiNb8gau-Ku2i5Fnh-J'
    return o
