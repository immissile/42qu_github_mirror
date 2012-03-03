#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.rss import  Rss, Zsite, RSS_PRE_PO, RSS_UNCHECK, RssPo
from zkit.single_process import single_process
from zkit.google.greader import Reader
from config import GREADER_USERNAME, GREADER_PASSWORD , DUMPLICATE_DB_PREFIX
from zkit.rss.txttidy import txttidy
from tidylib import  tidy_fragment
from zkit.htm2txt import htm2txt, unescape
from model.duplicate import Duplicator
from zweb.orm import ormiter
from model.po import Po, CID_NOTE
from zkit.bot_txt import txt_map
import traceback
from urllib import quote

def pre_br(txt):
    r = txt.replace('\r\n', '\n').replace('\r', '\n').replace('\n\n', '\n').replace('\n', '<br>')
    return r

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

def link_title_uid_txt(i):
    if 'alternate' in i:
        link = i['alternate'][0]['href']
    else:
        link = ''
    if 'title' in i:
        title = i['title']
        title = unescape(title)
    else:
        title = zsite.name
    rss_uid = i.get('id') or 1
    snippet = i.get('summary') or i.get('content') or None

    if not snippet:
        return

    if snippet:
        htm = snippet['content']
        if not htm:
            return

    htm = txttidy(htm)
    htm = txt_map('<pre', '</pre>', htm, pre_br)
    htm = tidy_fragment(htm, {'indent': 0})[0]
    htm = htm.replace('<br />', '\n')
    txt = htm2txt(htm)

    if not txt:
        return

    return link, title, rss_uid, txt

def rss_feed_update(res, id, user_id, limit=None):
    rss = Rss.mc_get(id)
    zsite = Zsite.mc_get(user_id)
    for count , i in enumerate(res):
        if limit:
            if count > limit:
                break
        r = link_title_uid_txt(i)
        if not r:
            continue
        link, title, rss_uid, txt = r

        if '相片: ' in title:
            continue


        title_txt = '%s\n%s'%(title, txt)
        if duplicator_rss.txt_is_duplicate(title_txt):
            continue

        #print title, link, duplicator_rss.txt_is_duplicate(title_txt)

        if rss.auto:
            state = RSS_PRE_PO
        else:
            state = RSS_UNCHECK

        c = RssPo.raw_sql(
'insert into rss_po (user_id,rss_id,rss_uid,title,txt,link,state) values (%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=%s , txt=%s ',
user_id, id, rss_uid, title, txt, link, state,
title, txt
        )
        duplicator_rss.set_record(title_txt, c.lastrowid)


def rss_subscribe(greader=None):
    from zkit.google.findrss import get_rss_link_title_by_url

    rss_list = []

    for i in Rss.where(gid=0):

        url = i.url.strip()
        #print url

        if not all((i.link, i.url, i.name)):
            rss, link, name = get_rss_link_title_by_url(url)
            #print link, name
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
            url = quote(i.url)
            try:
                greader.subscribe(url)
                i.gid = 1
                i.save()
            except:
                traceback.print_exc()
                print i.url, i.user_id
                i.delete()

            try:
                #print i.url
                feed = 'feed/%s'%url
                user_id = i.user_id
                duplicator_set_by_user_id(user_id)
                rss_feed_update(greader.feed(feed), i.id, user_id, 1024)
#                greader.mark_as_read(feed)
            except:
                traceback.print_exc()

    for i in Rss.where('gid<0'):
        if greader is None:
            greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
        try:
            greader.unsubscribe('feed/'+quote(i.url))
        except:
            traceback.print_exc()
            print i.url, i.user_id
        i.delete()

def duplicator_set_by_user_id(user_id):
    if not user_id:
        return
    for i in ormiter(Po, 'user_id=%s and cid=%s'%(user_id, CID_NOTE)):
        title_txt = '%s\n%s'%(i.name_, i.txt)
        if duplicator_rss.txt_is_duplicate(title_txt):
            #print i.name_
            continue
        duplicator_rss.set_record(title_txt, i.id)

@single_process
def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    rss_subscribe(greader)
    unread_update(greader)


if __name__ == '__main__':
    main()
    #greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    #for i in greader.feed('feed/%s'%'http://feed.feedsky.com/whitecrow_blog'):
    #    r = link_title_uid_txt(i)
    #    if r:
    #        link, title, rss_uid, txt = r
    #        title_txt = '%s\n%s'%(title, txt)
    #        if not duplicator_rss.txt_is_duplicate(title_txt):
    #            print title 

