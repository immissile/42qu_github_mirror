
#coding:utf-8

def prepare(o):
    o.SITE_DOMAIN = 'z32e1.tk' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.PORT = 31600

    o.SMTP = 'smtp.mailgun.org'
    o.SMTP_USERNAME = 'postmaster@z32.mailgun.org'
    o.SMTP_PASSWORD = '96ge3siyl1o7'
    o.SENDER_MAIL = o.SMTP_USERNAME
