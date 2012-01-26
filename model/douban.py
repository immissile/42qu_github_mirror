#!/usr/bin/env python
# -*- coding: utf-8 -*-

#douban_url
#id
#rid
#cid # 1 user 2 group 3 site
#url
#name

#douban_feed
#id
#cid
#rid
#rec         #推荐的人数
#like        #喜欢的人数
#user_id     
#topic_id    #小站 / 小组
#title            
#state       # 10. 达到推荐门槛, 但未审核  30. 审核未通过 60&40. 审核通过 , 抹去作者信息(比如原来就是转帖) 70&50. 审核通过 , 保留作者信息 
#html

#douban_user_feed
#id
#rid
#user_id
#cid       # 1 rec 2 like

#douban_rec
#id
#cid
#htm
#user_id

#需要定期重新抓取的 
#1. douban_feed    (一个月后在抓取一次即可, 一共也只需要抓取2次)
#2. 豆瓣用户的推荐 (现有的爬虫更新规则)
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM

DOUBAN_FEED_STATE_TO_REIVEW = 10 #达到推荐门槛, 但未审核  

CID_DOUBAN_FEED_NOTE = 1015
CID_DOUBAN_FEED_TOPIC = 1013

CID_DOUBAN_URL_USER = 1
CID_DOUBAN_URL_GROUP = 2
CID_DOUBAN_URL_SITE = 3

CID_DOUBAN_USER_FEED_LIKE = 1
CID_DOUBAN_USER_FEED_REC = 2


DOUBAN_REC_CID = {
    'photo_album':1,
    'doulist':2,
    'group':3,
    'artist':4,
    'url':5,
    'movie':6,
    'discussion':7,
    'online':8,
    'back':9,
    'review':10,
    'note':11,
    'topic':12,
    'book':13,
    'music':14,
    'entry':15,
    'site':16,
    'artist_video':17,
    'event':18,
    'photo':19,
}

mc_id_by_douban_url = McCache("IdByDoubanUrl:%s")
mc_id_by_douban_feed = McCache("IdByDoubanFeed:%s")

class DoubanUrl(Model):
    pass

class DoubanFeed(Model):
    pass

class DoubanUserFeed(Model):
    pass

class DoubanRec(Model):
    pass

def douban_user_feed_new(cid, rid, user_id):
    o = DoubanUserFeed.get_or_create(cid=cid, rid=rid, user_id=user_id)
    id = o.id
    o.save()
    return id


@mc_id_by_douban_url("{cid}_{url}")
def id_by_douban_url(cid, url):
    if type(url) in (int,long) or url.isdigit():
        sql = "select id from douban_url where cid=%s and rid=%s"
    else:
        sql = "select id from douban_url where cid=%s and url=%s"

    result = DoubanUrl.raw_sql( sql, cid , url).fetchone()
    if result:
        return result[0]

def user_id_by_douban_url(url):
    return id_by_douban_url(CID_DOUBAN_URL_USER, url)

def douban_url_new(cid, url, rid, name):
    if url == str(rid):
        url = ''
    o = DoubanUrl.get_or_create(cid=cid, rid=rid)
    o.url = url
    o.name = name
    o.save()
    return o.id

def douban_url_user_new(url, rid, name):
    douban_url_new(CID_DOUBAN_URL_USER, url, rid, name)

@mc_id_by_douban_feed("{cid}_{rid}")
def id_by_douban_feed(cid, rid):
    c = DoubanFeed.raw_sql("select id from douban_feed where cid=%s and rid=%s", cid, rid)
    r = c.fetchone()
    if r:
        return r[0]

def douban_rec_new(id, user_id, cid , htm):
    cid = DOUBAN_REC_CID.get(cid, 0)
    if not cid:
        return
    o = DoubanRec.get_or_create(id=id)
    o.htm = htm
    o.user_id = user_id
    o.cid = cid
    o.save()

def douban_feed_new(
    cid , rid , rec , like , title  , htm,  user_id=0, topic_id=0 
):
    o = DoubanFeed.get_or_create(cid=cid, rid=rid)
    o.rec = rec
    o.like = like
    if title:
        o.title = title
    if htm:
        o.htm = htm
    if user_id:
        o.user_id = user_id
    if topic_id:
        o.topic_id = topic_id

    if not o.state:
        state = 0
        if rec+like > 10 :
            state =  DOUBAN_FEED_STATE_TO_REIVEW
        o.state = state
    
    o.save()
    return o.id

if __name__ == '__main__':
    pass

