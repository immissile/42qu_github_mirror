from glob import glob
from os.path import exists
from mako.template import Template
from socket import gethostname

USER = glob('/home/z*')
USER = [
    int(i[7:]) for i in USER if i[7:].isdigit()
]

template = Template("""
#coding:utf-8

def prepare(o):
    o.SITE_DOMAIN = '${user}${hostname}.tk' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
    o.PORT = ${base_port}
   
    #参阅 http://book.42qu.com/mail/smtp.html , 申请一个免费的发邮件的SMTP 
    o.SMTP = ''
    o.SMTP_USERNAME = ''
    o.SMTP_PASSWORD = ''
    o.SENDER_MAIL = o.SMTP_USERNAME
""")

for id in USER:
    i = "z%s"%id
    filename = 'user/%s.py'%i
    if not exists(filename):
        print filename
        with open(filename, 'w') as user_z:
            base_port = id*50+30000
            user_z.write(
                template.render(
                    hostname = gethostname(), 
                    user=i, 
                    base_port=base_port
                )
            )

