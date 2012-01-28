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
#vote

#douban_rec
#id
#cid
#htm
#user_id

#需要定期重新抓取的 
#1. douban_feed    (一个月后在抓取一次即可, 一共也只需要抓取2次)
#2. 豆瓣用户的推荐 (现有的爬虫更新规则)
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from zkit.htm2txt import htm2txt, unescape
import re

DOUBAN_FEED_STATE_TO_REIVEW = 10 #达到推荐门槛, 但未审核  

CID_DOUBAN_FEED_NOTE = 1015
CID_DOUBAN_FEED_TOPIC = 1013


DOUBAN_USER_FEED_VOTE_LIKE = 1
DOUBAN_USER_FEED_VOTE_REC = 2



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

mc_id_by_douban_url = McCache('IdByDoubanUrl%s')
mc_id_by_douban_feed = McCache('IdByDoubanFeed%s')


#class ModelUrl(Model):
#    @classmethod
#    def id_by_url(cls, url):
#        if type(url) in (int, long) or url.isdigit():
#            return url    
#        tabel = cls.Meta.table 
#
#        sql = 'select id from %s url=%%s'%table
#
#        result = cls.raw_sql( sql , url).fetchone()
#        if result:
#            return result[0]
#
#
#    @classmethod
#    def new(cls, id, url, name):
#        if url == str(id):
#            url = ''
#
#        if url.isdigit():
#            id = int(url)
#            url = ''
#
#        o = None
#        if id:
#            o = cls.get(id)
#
#        if o is None and url:
#            o = cls.get(url=url)
#
#        o.id = id
#
#        if url:
#            o.url = url
#
#        if name:
#            o.name = name
#
#        o.save()
#
#        return id

class DoubanUser(Model):
    pass
class DoubanGroupUid(Model):
    pass
class DoubanUserToFetch(Model):
    pass
class DoubanFeed(Model):
    pass
class DoubanUserFeed(Model):
    pass
class DoubanRec(Model):
    pass

def douban_user_feed_new(vote, cid, rid, user_id):
    o = DoubanUserFeed.get_or_create(cid=cid, rid=rid, user_id=user_id)
    id = o.id
    o.save()
    return id




def user_id_by_url(url):
    return id_by_url(DoubanUser, url)


#def douban_user_new(url, id, name):
#    return douban_url_new(DoubanUser, url, id, name)

@mc_id_by_douban_feed('{cid}_{rid}')
def id_by_douban_feed(cid, rid):
    c = DoubanFeed.raw_sql('select id from douban_feed where cid=%s and rid=%s', cid, rid)
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
    cid , rid , rec , like , title  , htm, user_id=0, topic_id=0
):
    o = DoubanFeed.get_or_create(cid=cid, rid=rid)
    o.rec = rec
    o.like = like
    if title:
        o.title = title
    if htm:
        o.htm = htm.replace("<wbr>","")
    if user_id:
        o.user_id = user_id
    if topic_id:
        o.topic_id = topic_id

    if not o.state:
        state = 0
        if int(rec)+int(like) > 10 :
            state = DOUBAN_FEED_STATE_TO_REIVEW
        o.state = state

    o.save()
    return o.id


RE_ZT = re.compile('(?!A-Z)ZT(?!A-Z)')

def title_normal(title):
    title = unescape(title)
    title = RE_ZT.sub('转', title)
    title = ' %s '%title.strip()
    title = title\
            .replace('【', '[')\
            .replace('】', ']')\
            .replace('［', '[')\
            .replace('］', ']')\
            .replace('（', '(')\
            .replace('）', ')')\
            .replace('：', ':')\
            .replace('转发', '转')\
            .replace('-转', '转')\
            .replace('转帖', '转')\
            .replace('转贴', '转')\
            .replace('转载', '转')\
            .replace('转:', '')\
            .replace('《转》', '')\
            .replace('[转]', '')\
            .replace('(转)', '')\
            .replace('转)', '')\
            .replace(' 转 ', '')\
            .replace('。转', '')\
            .replace('》转', '》')\
            .strip()
    return title

if __name__ == '__main__':
#    print dir(DoubanUser.table)
#    print user_id_by_douban_url("catcabinet")
#    print len("在非相对论系统中，粒子运动速度远小于光速，它们间的相互作用仍很频繁，参与相互作用的粒子数目较多")
#    raise
#    pass
#    is_douban_count = 0
#    not_douban_count = 0
#
#    for i in sorted(DoubanFeed.where(state=DOUBAN_FEED_STATE_TO_REIVEW), key=lambda x:-x.rec-x.like):
#        txt = '\n'.join([i.title, i.htm])
#        is_douban = False
#
#        for word in ('豆瓣', '豆邮', '豆友', '?start=', '>http://www.douban.'):
#            if word in txt:
#                is_douban = True
#                break
#
#        if is_douban:
#            is_douban_count += 1
#        else:
#            not_douban_count += 1
#
#        if not is_douban:
#
#            if i.cid == CID_DOUBAN_FEED_TOPIC:
#                link = 'http://www.douban.com/group/topic/%s'%i.rid
#            elif i.cid == CID_DOUBAN_FEED_NOTE:
#                link = 'http://www.douban.com/note/%s'%i.rid
#
#            print '%60s %5s %5s %s'%( link, i.rec, i.like, title_normal(i.title))
#
#    print is_douban_count, not_douban_count


#    for i in """
#TRUNCATE TABLE  douban_feed;
#TRUNCATE TABLE  douban_rec;
#TRUNCATE TABLE  douban_user_feed;
#TRUNCATE TABLE  douban_group;
#TRUNCATE TABLE  douban_site;
#TRUNCATE TABLE  douban_user;
#    """.strip().split(";"):
#        if i.strip():
#            DoubanFeed.raw_sql(i.strip()+";")
