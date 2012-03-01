#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.rss import rss_subscribe, Rss, Zsite, RSS_PRE_PO, RSS_UNCHECK, RssPo
from zkit.single_process import single_process
from zkit.google.greader import Reader
from config import GREADER_USERNAME, GREADER_PASSWORD, 
from zkit.rss.txttidy import txttidy
from tidylib import  tidy_fragment
from zkit.htm2txt import htm2txt, unescape
from model.duplicate import Duplicator

duplicator_rss = Duplicator(DUMPLICATE_DB_PREFIX%'rss')

def unread_update(greader=None):
    if greader is None:
        greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

    feeds = greader.unread_feed()

    for feed in feeds:
        try:
            unread_feed_update(greader, feed)
        except:
            traceback.print_exc()
            continue

    greader.mark_as_read()


def unread_feed_update(greader, feed):
    rs = Rss.raw_sql('select id,user_id from rss where url = %s', feed[5:]).fetchone()
    if rs:
        id, user_id = rs

        res = greader.unread(feed)
        rss_feed_update(res, id , user_id)


def rss_feed_update(res, id, user_id, limit=None):
    rss = Rss.mc_get(id)
    zsite = Zsite.mc_get(user_id)
    for count , i in enumerate(res):
        if limit:
            if count > limit:
                break
        if 'alternate' in i:
            link = i['alternate'][0]['href']
        else:
            link = ''
        if 'title' in i:
            title = i['title']
        else:
            title = zsite.name
        rss_uid = i.get('id') or 1
        snippet = i.get('summary') or i.get('content') or None

        if snippet:
            htm = snippet['content']
            if htm:
                htm = txttidy(htm)
                htm = txt_map('<pre', '</pre>', htm, pre_br)
                htm = tidy_fragment(htm, {'indent': 0})[0]
                htm = htm.replace('<br />', '\n')
                txt = htm2txt(htm)

                if txt:
                    title = unescape(title)
                    
                    title_txt"%s\n%s"%(title, txt)
                    if duplicator_rss.txt_is_duplicate(title_txt):
                        continue 

                    if rss.auto:
                        state = RSS_PRE_PO
                    else:
                        state = RSS_UNCHECK

                    c = RssPo.raw_sql(
'insert into rss_po (user_id,rss_id,rss_uid,title,txt,link,state) values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=%s , txt=%s ',
user_id, id, rss_uid, title, txt, link,  state,
title, txt
                    )
                    duplicator_rss.set_record(title_txt, c.lastrowid)


def rss_subscribe(greader=None):
    from zkit.google.findrss import get_rss_link_title_by_url

    rss_list = []

    for i in Rss.where(gid=0):

        url = i.url.strip()

        if not all((i.link, i.url, i.name)):
            rss, link, name = get_rss_link_title_by_url(url)

            if rss:
                i.url = rss

            if link:
                i.link = link

                if not name:
                    name = link.split('://', 1)[-1]

            if name:
                i.name = name

            i.save()

        rss_list.append(i)

    if rss_list:
        if greader is None:
            greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

        for i in rss_list:
            #print i.url
            try:
                greader.subscribe(i.url)
                i.gid = 1
                i.save()
                #print i.url
                feed = 'feed/%s'%i.url
                rss_feed_update(greader.feed(feed), i.id, i.user_id, 1024)
                greader.mark_as_read(feed)
            except:
                traceback.print_exc()
                print i.url, i.user_id
                i.delete()

    for i in Rss.where('gid<0'):
        if greader is None:
            greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
        greader.unsubscribe('feed/'+i.url)
        #print "unsubscribe",i.url
        i.delete()



@single_process
def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    rss_subscribe(greader)
    unread_update(greader)


if __name__ == '__main__':
    main()
