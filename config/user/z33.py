
#coding:utf-8

def prepare(o):
    o.SITE_DOMAIN = 'z33e1.tk' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.PORT = 31650
   
    o.SMTP = 'smtp.mailgun.org'
    o.SMTP_USERNAME = 'postmaster@z33.mailgun.org'
    o.SMTP_PASSWORD = '6a433suwib56'
    o.SENDER_MAIL = o.SMTP_USERNAME
    
    o.ZDATA_PATH = "/home/z33/file/"
