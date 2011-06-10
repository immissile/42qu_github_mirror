#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from greader import Reader
from private import password
from os.path import exists, abspath, dirname, join
from os import makedirs as _makedirs

DUMP_DIR = join(dirname(abspath(__file__)), "dump")

def makedirs(dirpath):
    if not exists(dirpath):
        _makedirs(dirpath)

reader = Reader('zsp007@gmail.com', password)

for i in reader.feed():
#    print i.keys()
    print i['title']
    if u'content' in i:
        content = i['content']
    elif u'summary' in i:
        content = i['summary']
    else:
        continue

    id = i['id'][len('tag:google.com,2005:reader/item/'):]

    dirpath = open(join(DUMP_DIR,id[:2],id[2:4]))

    makedirs(dirpath)

    with open(join(dirpath,"%s.html"%id)) as outfile:
        outfile.write("""<!doctype html><html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>%s</title></head>
<body style="width:720px;margin:auto;font-size:16px;line-height:28px">
<h1 style="font-weight::16px;text-align:center">%s</h1>
%s
</body>
"""%(
    title,
    title,
    content['content']
)
)


