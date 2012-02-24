#coding:utf-8
import _env
from json import loads
from zkit.htm2txt import htm2txt
from config import ZSITE_UCD_CHINA_ID
#{u'origin': {u'streamId': u'feed/http://ucdchina.com/rss/category?id=1', u'htmlUrl': u'http://ucdchina.com/rss/category?id=1', u'title': u'\u4ea7\u54c1\u5e02\u573a - UCD\u5927\u793e\u533a'}, u'updated': 1322773790, u'isReadStateLocked': True, u'author': u'\u80d6\u80e1\u6590', u'title': u'\u80d6\u80e1\u6590\u8bf4\u6dd8\u5b9d\u4fc3\u9500\u4e4b\u4e00\uff1a\u4fc3\u9500\u4e4b\u201c\u5546\u201d', u'alternate': [{u'href': u'http://ucdchina.com/snap/11171', u'type': u'text/html'}], u'timestampUsec': u'1322773790821277', u'comments': [], u'summary': {u'content': 
#


with open('/mnt/zdata/ucd_china.js') as ucd_china:
    for line in ucd_china:
        line = loads(line)
        title = line['title']

        if u'书友会' in title:
            continue
        if u'author' in line:
            author = line['author']
        else:
            author = ''
        if u'content' in line:
            content = line['content']
        elif u'summary' in line:
            content = line['summary']
        else:
            continue
        link = line['alternate'][0]['href']
        content = content['content']

        content = str(htm2txt(content)) 
        source = content.find("源地址：")
        if source >= 0:
            slink = content[source:].split("\n",1)[0].strip()
            slink = slink[slink.find("http"):]
            content = content[:source]
            link = slink

        if len(content)<2000:
            continue
    
        print author, title, link

        #10109232

#        print title
#        print content
#print htm2txt( content )


