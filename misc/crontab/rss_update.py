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


@single_process
def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    rss_subscribe(greader)
    unread_update(greader)


if __name__ == '__main__':
    main()
