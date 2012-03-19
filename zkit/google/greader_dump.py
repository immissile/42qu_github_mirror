#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from urlparse import urlparse
from greader import Reader
from private import password
from os.path import exists, abspath, join
from os import makedirs as _makedirs

DUMP_DIR = join('/mnt/share', 'zsp_google_reader')

def makedirs(dirpath):
    if not exists(dirpath):
        _makedirs(dirpath)

reader = Reader('zsp007@gmail.com', password)

for subscription, i in reader.subscription_item_dump():
#    print i.keys()
    if u'content' in i:
        content = i['content']
    elif u'summary' in i:
        content = i['summary']
    else:
        continue
    dirpath = urlparse(subscription[5:]).netloc.split(':')[0]

    if u'title' not in i:
        continue

    id = i['id'][len('tag:google.com,2005:reader/item/'):]

    dirpath = join(DUMP_DIR, dirpath or '0')
    title = i['title']

    makedirs(dirpath)

    with open(join(dirpath, '%s.html'%id), 'w') as outfile:
        outfile.write("""<!doctype html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>%s</title></head>
<body style="width:800px;font-family:Tahoma,Verdana;margin:auto;font-size:16px;line-height:28px;padding-bottom:64px">
<h1 style="font-family:微软雅黑;font-size:32px;line-height:48px;font-family:Georgia;text-align:center;font-weight:normal;margin:48px 0">%s</h1>
%s
</body>
""" % (
        title,
        title,
        content['content']
)
)


