def prepare(o):
    o.SITE_DOMAIN = 'motionio.us' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.PORT = 31800
   
    o.SMTP = 'smtp.mailgun.org'
    o.SMTP_USERNAME = 'postmaster@wooparadog.mailgun.org'
    o.SMTP_PASSWORD = '2zcpxlnii6x0'
    o.SENDER_MAIL = o.SMTP_USERNAME

    o.ZDATA_PATH = "/home/z36/file/"
