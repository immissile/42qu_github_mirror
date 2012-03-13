from glob import glob
from os.path import exists
from mako.template import Template
from socket import gethostname

USER = glob('/home/z*')
USER = [
    i[6:] for i in USER if i[7:].isdigit()
]

template = Template("""
#coding:utf-8

def prepare(o):
    o.SITE_DOMAIN = '${user}${hostname}.tk' 
    o.FILE_DOMAIN = 'p.%s'%o.SITE_DOMAIN
    o.FS_DOMAIN = 's.%s'%o.SITE_DOMAIN
""")

for i in USER:
    filename = 'user/%s.py'%i
    if not exists(filename):
        print filename
        with open(filename, 'w') as user_z:
            user_z.write(
                template.render(hostname = gethostname(), user=i)
            )

