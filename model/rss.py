#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from zkit.google.greader import Reader  
import json


class Rss(McModel):
    pass

class PrePo(McModel):
    pass


GREADER = Reader('42qu.com@gmail.com','42qukanrss')

def rss_add(user_id,url):
    Rss.raw_sql('insert into rss (user_id, url) values(%s, %s)',user_id,url)

def get_unread_update():
    feeds = GREADER.unread_feed()
    for feed in feeds:
        rs = Rss.raw_sql('select id,user_id in rss where url = %s',feed[5:]).fetchone()[0]
        if rs:
            id,user_id = rs
            res = GREADER.unread(feed)
            for i in res:
                link = i['alternate'][0]['href']
                title = i['title']
                rss_uid = i.get('id') or None
                snippet = i.get('summary') or i.get('content') or None
                if snippet:
                    txt = snippet['content']
                else:
                    txt = ""
                PrePo.raw_sql('insert into pre_po (user_id,rss_id,rss_uid,title,htm,state) value(%s,%s,%s,%s,%s,0)',user_id,id,rss_uid,title,txt)

def get_rss_json(url):
    feeds = GREADER.unread(url)
    i = feeds.next()
    link = i['alternate'][0]['href']
    title = i['title']
    snippet = i.get('summary') or i.get('content') or None
    if snippet:
        txt = snippet['content']
    else:
        snippet = ""
        txt = ""
    stamp = int(i['crawlTimeMsec'])/1000
    print link,title,i['id']



if __name__ == "__main__":
    #get_rss_json('feed/http://feed43.com/rexsong.xml')
    #rss_feed()



