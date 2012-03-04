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
        title = '无题'
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

def rss_tag():
    from model.rss import RSS_PO_ID_STATE_NOTAG, CID_USER, RssPoId, RSS_PO_ID_STATE_AUTOTAG
    from zweb.orm import ormiter
    from zdata.idf.tfidf import tag_id_rank_list_by_txt, ID2NAME
    from model.po import Po
    from operator import itemgetter
    from model.po_tag_user import tag2idlist_po_user, rss_po_new
    from zkit.algorithm.unique import unique

    for rss_po_id in ormiter(
        RssPoId,
        'user_cid=%s and state=%s'%(CID_USER, RSS_PO_ID_STATE_NOTAG)
    ):
        po = Po.mc_get(rss_po_id.po_id)
        if not po:
            continue

        #print po.name_

        txt = '%s\n%s'%(po.name_, po.txt)
        tag_id_rank_list = tag_id_rank_list_by_txt(txt)[:7]
        tag_id_list = map(itemgetter(0), tag_id_rank_list)
        user_tag_id_list = map(
            int,
            tag2idlist_po_user.tag_id_list_by_id(
                po.user_id
            )
        )
        id_list = user_tag_id_list[:]
        id_list.extend(tag_id_list)
        rss_po_id.tag_id_list = ' '.join(
            map(str, unique(id_list))
        )

        #for i in tag_id_list:
        #    i.append_id_tag_id_list
        #print i.tag_id_list 
        #raise
        rss_po_id.state = RSS_PO_ID_STATE_AUTOTAG
        rss_po_id.save()

        rss_po_new(po, user_tag_id_list)

def main():
    greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    rss_subscribe(greader)
    unread_update(greader)
    rss_tag()

if __name__ == '__main__':
    main()


    #from model.rss import RSS_PO_ID_STATE_NOTAG, CID_USER, RssPoId, RSS_PO_ID_STATE_AUTOTAG
    #RssPoId.where(state=RSS_PO_ID_STATE_AUTOTAG).update(state=RSS_PO_ID_STATE_NOTAG)
    #greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    #for i in greader.feed('feed/%s'%'http://feed.feedsky.com/whitecrow_blog'):
    #    r = link_title_uid_txt(i)
    #    if r:
    #        link, title, rss_uid, txt = r
    #        title_txt = '%s\n%s'%(title, txt)
    #        if not duplicator_rss.txt_is_duplicate(title_txt):
    #            print title 

#    from model.rss import RSS_PO_ID_STATE_NOTAG, CID_USER, RssPoId, RSS_PO_ID_STATE_AUTOTAG
#    from zweb.orm import ormiter
#    from zdata.idf.tfidf import tag_id_rank_list_by_txt, ID2NAME
#    from model.po import Po
#    from operator import itemgetter
#    from model.po_tag_user import tag2idlist_po_user, rss_po_new
#    from zkit.algorithm.unique import unique
#    from model.zsite import Zsite
#
#    no_tag = set()
#    for rss_po_id in ormiter(
#        RssPoId,
#        'user_cid=%s'%(CID_USER)
#    ):
#        tag = tag2idlist_po_user.tag_id_list_by_id(
#            rss_po_id.user_id
#        )
#        if not tag:
#            no_tag.add(rss_po_id.user_id)
#
#    for pos, i in enumerate(Zsite.mc_get_list(no_tag)):
#        print pos , i.id, i.name
#        print 'http:'+i.link
#        print ""
#

