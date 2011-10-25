def prepare(o):
    o.SITE_DOMAIN = 'yup.xxx'
    o.PORT = 30300
    o.MYSQL_MAIN = 'zpage'
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.RENREN_CONSUMER_KEY = '5bba3dbbb90842678e3873fccb00dc3c'
    o.RENREN_CONSUMER_SECRET = '6f7226df5c804053abf523080387f2b0'
    o.GOOGLE_CONSUMER_KEY = '518129477934.apps.googleusercontent.com'
    o.GOOGLE_CONSUMER_SECRET = 'FRWbGhiNb8gau-Ku2i5Fnh-J'
    return o
