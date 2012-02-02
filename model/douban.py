#!/usr/bin/env python
# -*- coding: utf-8 -*-


#需要定期重新抓取的 
#1. douban_feed    (一个月后在抓取一次即可, 一共也只需要抓取2次)
#2. 豆瓣用户的推荐 (现有的爬虫更新规则)
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, mc
from zkit.htm2txt import htm2txt, unescape
import re

DOUBAN_FEED_STATE_TO_REIVEW = 10 #达到推荐门槛, 但未审核  
DOUBAN_FEED_STATE_REVIEWED = 20

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
mc_model_url = '%s.%s'

class ModelUrl(object):
    @classmethod
    def new(cls, id, url, name):
        if url == str(id):
            url = ''

        if url.isdigit():
            id = int(url)
            url = ''

        o = None
        if id:
            o = cls.mc_get(id)

        if o is None and url:
            o = cls.get(url=url)

        if o is None:
            o = cls()

        o.id = id

        if url:
            o.url = url
            #print url
            key = mc_model_url%(cls.__name__ , url)
            mc.set(key, id)
        key = mc_model_url%(cls.__name__ , id)
        mc.set(key, id)

        if name:
            o.name = name

        o.save()

        return o

    @classmethod
    def by_url(cls, url):
        key = mc_model_url%(cls.__name__ , url)
        id = mc.get(key)
        if id is None:
            if type(url) in (int, long) or url.isdigit():
                o = cls.mc_get(url)
                if o:
                    id = o.id
            else:
                o = cls.get(url=url)
                if o:
                    id = o.id
        mc.set(key, id or 0)
        return id

class DoubanUser(McModel, ModelUrl):
    pass
class DoubanGroup(McModel, ModelUrl):
    pass
class DoubanFeed(Model):
    @property
    def link(self):
        if self.cid == CID_DOUBAN_FEED_TOPIC:
            link = 'http://www.douban.com/group/topic/%s'%self.rid
        elif self.cid == CID_DOUBAN_FEED_NOTE:
            link = 'http://www.douban.com/note/%s'%self.rid
        return link

class DoubanUserFeed(Model):
    pass
class DoubanRec(Model):
    pass
class DoubanFeedOwner(Model):
    pass


def douban_user_feed_new(vote, cid, rid, user_id):
    o = DoubanUserFeed.get_or_create(cid=cid, rid=rid, user_id=user_id)
    id = o.id
    o.save()
    return id


def douban_user_by_feed_id(id):
    feed = DoubanFeed.get(id)
    if feed:
        user = DoubanUser.get(feed.user_id)
        #print user, feed.user_id
        if user:
            return user
    

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

def douban_rec_new(id, user_id, cid , htm, time):
    o = DoubanRec.get_or_create(id=id)
    o.htm = htm
    o.user_id = user_id
    o.cid = cid
    o.time = time
    o.save()

def douban_feed_new(
    cid , rid , rec , like , title  , htm, time, user_id=0, topic_id=0
):
    o = DoubanFeed.get_or_create(cid=cid, rid=rid)
    o.rec = rec
    o.like = like
    if title:
        o.title = title_normal_sign(title)
    if htm:
        o.htm = htm.replace('<wbr>', '')
    if user_id:
        o.user_id = user_id
    if topic_id:
        o.topic_id = topic_id

    if not o.state:
        state = 0
        if int(rec)+int(like) > 20 :
            state = DOUBAN_FEED_STATE_TO_REIVEW
        o.state = state
    o.time = time
    o.save()
    return o.id


RE_ZT = re.compile('(?!A-Z)ZT(?!A-Z)')

def title_normal_sign(title):
    title = unescape(title)\
            .replace('【', '[')\
            .replace('】', ']')\
            .replace('［', '[')\
            .replace('］', ']')\
            .replace('（', '(')\
            .replace('）', ')')\
            .replace('：', ':').strip()

    return title

def title_normal_rt(title):
    title = RE_ZT.sub('转', title)
    title = ' %s '%title.strip()
    title = title\
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

def douban_feed_to_review_iter():
    from zweb.orm import ormiter
    for i in ormiter(
        DoubanFeed,
        'state = %s'%DOUBAN_FEED_STATE_TO_REIVEW
    ):
        i.state = DOUBAN_FEED_STATE_REVIEWED
        i.save()
        yield i

def is_rt_by_title(title):
    t = title_normal_sign(title)
    return title_normal_rt(t)==t

def title_normal(title):
    return title_normal_rt(title_normal_sign(title))

if __name__ == '__main__':
    pass
    txt='教你怎样成为K歌之王，几天改变你的嗓音!!!（附内部练习＋教学视频）'
    print title_normal(txt)
    #kv_int.set(KV_IMPORT_DOUBAN,0)
    #douban_feed_to_review_iter()
    #for i in DoubanFeed.where('state = %s',DOUBAN_FEED_STATE_TO_REIVEW):
    #    total = i.rec + i.like
    #    if total < 2000:
    #        i.state = 0
    #        i.save()
    #    else:
    #        print title_normal_rt(i.title)
#    for i in DoubanFeed.where('state = %s',DOUBAN_FEED_STATE_TO_REIVEW):
#        total = i.rec + i.like
#        if total < 2000:
#            i.state = 0
#            i.save()
#        else:
#            print title_normal_rt(i.title)

    #print douban_feed_to_review_iter()
    print 'DoubanUser.count()', DoubanUser.count()
    print 'DoubanFeed.count()', DoubanFeed.count()

#   # print DoubanUser.by_url('zuroc')
#   #from zweb.orm import ormiter
#   #for i in ormiter(DoubanUser):
#   #    print i.id, i.name, i.url
#   # print dir(DoubanUser.table)
#   # print user_id_by_douban_url("catcabinet")
#   # print len("在非相对论系统中，粒子运动速度远小于光速，它们间的相互作用仍很频繁，参与相互作用的粒子数目较多")
#   # raise
#   # pass
    #is_douban_count = 0
    #not_douban_count = 0

    #for i in sorted(DoubanFeed.where(state=DOUBAN_FEED_STATE_TO_REIVEW), key=lambda x:-x.rec-x.like):
    #    txt = '\n'.join([i.title, i.htm])
    #    is_douban = False

    #    for word in ('豆瓣', '豆邮', '豆友', '?start=', '>http://www.douban.'):
    #        if word in txt:
    #            is_douban = True
    #            break

    #    if is_douban:
    #        is_douban_count += 1
    #    else:
    #        not_douban_count += 1

    #    if not is_douban:

    #        if i.cid == CID_DOUBAN_FEED_TOPIC:
    #            link = 'http://www.douban.com/group/topic/%s'%i.rid
    #        elif i.cid == CID_DOUBAN_FEED_NOTE:
    #            link = 'http://www.douban.com/note/%s'%i.rid

    #        print '%60s %5s %5s %s %s'%( link, i.rec, i.like, title_normal_rt(i.title), len(i.htm))

    #print is_douban_count, not_douban_count

#
##    print DoubanUser.by_url('zuroc')
##   from zweb.orm import ormiter
##   for i in ormiter(DoubanUser):
##       print i.id, i.name, i.url
##    print dir(DoubanUser.table)
##    print user_id_by_douban_url("catcabinet")
##    print len("在非相对论系统中，粒子运动速度远小于光速，它们间的相互作用仍很频繁，参与相互作用的粒子数目较多")
##    raise
##    pass
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
#            print '%60s %5s %5s %s %s'%( link, i.rec, i.like, title_normal_rt(i.title), len(i.htm))
#
#    print is_douban_count, not_douban_count
#
#
##    for i in """
##TRUNCATE TABLE douban_feed
##TRUNCATE TABLE douban_feed_owner
##TRUNCATE TABLE douban_rec
##TRUNCATE TABLE douban_user
##TRUNCATE TABLE douban_user_feed 
##    """.strip().split('\n'):
##        if i.strip():
##            DoubanFeed.raw_sql(i.strip()+';')
