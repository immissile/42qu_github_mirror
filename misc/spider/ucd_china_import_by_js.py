#coding:utf-8
import _env
from json import loads
from zkit.htm2txt import htm2txt
from config import ZSITE_UCD_CHINA_ID
from misc.crontab.feed_import import feed_import_new, PoMetaUser, FeedImport
from urllib import quote
#{u'origin': {u'streamId': u'feed/http://ucdchina.com/rss/category?id=1', u'htmlUrl': u'http://ucdchina.com/rss/category?id=1', u'title': u'\u4ea7\u54c1\u5e02\u573a - UCD\u5927\u793e\u533a'}, u'updated': 1322773790, u'isReadStateLocked': True, u'author': u'\u80d6\u80e1\u6590', u'title': u'\u80d6\u80e1\u6590\u8bf4\u6dd8\u5b9d\u4fc3\u9500\u4e4b\u4e00\uff1a\u4fc3\u9500\u4e4b\u201c\u5546\u201d', u'alternate': [{u'href': u'http://ucdchina.com/snap/11171', u'type': u'text/html'}], u'timestampUsec': u'1322773790821277', u'comments': [], u'summary': {u'content': 
#

for i in FeedImport.where(zsite_id=ZSITE_UCD_CHINA_ID):
    txt = i.txt
    txt = txt.split("\n")
    r = []
    for line in txt:
        if 'www1.feedsky.com' not in line:
            r.append(line)
    txt = "\n".join(r)
    print txt

raise
with open('/mnt/zdata/ucd_china.js') as ucd_china:
    for line in ucd_china:
        line = loads(line)
        title = line['title']

        if u'书友会' in title:
            continue
        if u'author' in line:
            author = line['author']
        else:
            continue
 
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
    

        user = PoMetaUser.get_or_create(name=author, cid=ZSITE_UCD_CHINA_ID)
        if not user.id:
            user.url = 0 
            user.save()
            user.url = user.id
            user.save() 
        
        feed_import_new(
            ZSITE_UCD_CHINA_ID, user.id, title, content, link,  len(content)/3
        )
        print user.id
        #10109232

#        print title
#        print content
#print htm2txt( content )


