
#coding:utf-8

def prepare(o):
    o.SITE_DOMAIN = 'z33e1.tk' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.PORT = 31650
   
    #参阅 http://book.42qu.com/mail/smtp.html , 申请一个免费的发邮件的SMTP 
    o.SMTP = ''
    o.SMTP_USERNAME = ''
    o.SMTP_PASSWORD = ''
    o.SENDER_MAIL = o.SMTP_USERNAME
