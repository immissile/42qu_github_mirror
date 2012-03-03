#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from zkit.google.greader import Reader
import json
import sys
from config import GREADER_USERNAME, GREADER_PASSWORD, ADMIN_MAIL
import traceback
from model.mail import rendermail
from model.user_mail import mail_by_user_id
from model.zsite import Zsite
from model.cid import CID_USER

RSS_UNCHECK = 0
RSS_RM = 1
RSS_PRE_PO = 2
RSS_RT_PO = 3
RSS_POED = 4
RSS_SYNC = 5

STATE_RSS_NEW = 5
STATE_RSS_EMAILD = 6
STATE_RSS_REJECT = 7
STATE_RSS_OK = 8



STATE2CN = {
    STATE_RSS_OK:'通过',
    STATE_RSS_NEW:'新建',
    STATE_RSS_EMAILD:'已经联系',
    STATE_RSS_REJECT:'已经被拒绝'
}

RSS_PO_ID_STATE_NOTAG = 0
RSS_PO_ID_STATE_AUTOTAG = 10
RSS_PO_ID_STATE_TAGED = 20

class RssPoId(Model):
    pass

def rss_po_id_new(user, rss_po_id, po_id):
    RssPoId.raw_sql(
        'insert delayed into rss_po_id '\
        '(rss_po_id, po_id, user_id, user_cid, state) '\
        'values (%s, %s, %s, %s, %s)', 
        rss_po_id, po_id,  user.id, user.cid, RSS_PO_ID_STATE_NOTAG,
    )

mc_rss_link_by_po_id = McCache('RssLinkByPoId:%s')

@mc_rss_link_by_po_id('{id}')
def rss_link_by_po_id(id):
    rss_po = RssPoId.get(po_id=id)
    if rss_po:
        rss_po = RssPo.mc_get(rss_po.id)
        if rss_po:
            return rss_po.link



class Rss(McModel):
    pass

class RssPo(McModel):
    pass


class RssUpdate(McModel):
    pass

def rss_po_total(state):
    return RssPo.where(state=state).count()

def rss_new(user_id, url, name=None, link=None, gid=0, auto=0):
    rss = Rss.get_or_create(url=url)
    rss.user_id = user_id
    rss.gid = gid
    if name:
        rss.name = name
    if link:
        rss.link = link
    rss.auto = int(bool(auto))
    rss.save()
    return rss

def rss_update_new(id, state):
    rss = RssUpdate.get_or_create(id=id)
    rss.state = state
    rss.save()
    return rss


def rss_total_gid(gid):
    return Rss.where(gid=gid).count()

def get_rss_by_gid(gid, limit=1, offset=10):
    rss = Rss.raw_sql('select id,user_id,url,gid,name,link from rss where gid = %s order by id desc limit %s offset %s', gid, limit, offset).fetchall()
    return rss

def rss_po_list_by_state(state, limit=1, offset=10):
    p = RssPo.raw_sql('select id,link,user_id,title,txt,rss_id from rss_po where state = %s order by id desc limit %s offset %s', state, limit, offset).fetchall()
    return p


def mail_by_rss_id(rss_id):
    rss = Rss.mc_get(rss_id)
    zsite = Zsite.mc_get(rss.user_id)
    if zsite and zsite.cid == CID_USER:
        mail = mail_by_user_id(rss.user_id)
        if not mail:
            return

        rendermail(
            '/mail/notice/invite_blog.txt',
            mail,
            zsite.name,
            sender=ADMIN_MAIL
        )

        ru = RssUpdate.mc_get(rss_id)
        if ru:
            ru.state = STATE_RSS_EMAILD
            ru.save()
        else:
            rss_update_new(rss_id, STATE_RSS_EMAILD)




<<<<<<< local
=======
def rss_subscribe(greader=None):
    from zkit.google.findrss import get_rss_link_title_by_url

    rss_list = []

    for i in Rss.where(gid=0):

        url = i.url.strip()

        #print url
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
                rss_feed_update(greader.feed(feed), i.id, i.user_id, 512)
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


>>>>>>> other
if __name__ == '__main__':
    pass

#    from zkit.rss.txttidy import txttidy
#    from tidylib import  tidy_fragment
    rss = Rss.get(596)
    print rss.id, rss.gid


    for i in Rss.where("gid<0"):
        print i

