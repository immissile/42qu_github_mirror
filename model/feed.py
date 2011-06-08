#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from mq import mq_client

MAXINT = sys.maxint
PAGE_LIMIT = 42
FEED_ENTRY_ID_LASTEST_SQL = "select id from feed_entry where feed_id=%%s order by id desc limit %s"%PAGE_LIMIT
FEED_ENTRY_ID_ITER_SQL = "select id from feed_entry where feed_id=%%s and id<%%s order by id desc limit %s"%PAGE_LIMIT

mc_feed_id_list_by_zsite_id = McCacheA("FeedIdByZsiteId:%s")
mc_feed_id_by_for_zsite_follow = McCacheA("FeedIdForZsiteFollow<%s")
mc_feed_entry_tuple = McCacheM("FeedEntryTuple:%s")
mc_feed_entry_iter = McCacheA("FeedEntryIter:%s")
mc_feed_id_by_zsite_id_cid = McCache("FeedIdByZsiteIdCid:%s")

cursor = cursor_by_table('feed_entry')

class Feed(McModel):
    pass

@mc_feed_id_by_zsite_id_cid("{zsite_id}_{cid}")
def feed_id_by_zsite_id_cid(zsite_id, cid):
    feed = Feed.get_or_create(zsite_id=zsite_id, cid=cid)
    if not feed.id:
        feed.save()
        mc_feed_id_list_by_zsite_id.delete(zsite_id)
        mq_mc_flush_zsite_follow(zsite_id)
    return feed.id


def feed_entry_new(id, zsite_id, cid):
    feed_id = feed_id_by_zsite_id_cid(zsite_id, cid)
    cursor.execute(
        "insert into feed_entry (id, feed_id) values (%s,%s) on duplicate key update id=id",
        (id, feed_id)
    )
    cursor.connection.commit()
    mc_feed_entry_iter.delete(feed_id)
    return id

def feed_entry_rm(id):
    cursor.execute("select feed_id from feed_entry where id=%s", id)
    r = cursor.fetchone()
    if r:
        feed_id = r[0]
        cursor.execute("delete from feed_entry where id=%s", id)
        cursor.connection.commit()
        mc_feed_entry_iter.delete(feed_id)

@mc_feed_entry_iter("{feed_id}")
def feed_entry_id_lastest(feed_id):
    cursor.execute(FEED_ENTRY_ID_LASTEST_SQL, feed_id)
    return [
        i for i, in cursor
    ]


#TODO : 消息流的合并, feed_entry_id_iter 函数可以考虑用天涯的内存数据库来优化
#http://code.google.com/p/memlink/
def feed_entry_id_iter(id, start_id=MAXINT, ):
    if start_id == MAXINT:
        id_list = feed_entry_id_lastest(id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i
        else:
            return
    while True:
        cursor.execute(FEED_ENTRY_ID_ITER_SQL, (id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i, in c:
            yield i
        start_id = i


def feed_entry_cmp_iter(id, start_id=sys.maxint):
    for i in feed_entry_id_iter(id, start_id):
        yield FeedEntryCmp(id, i)

class FeedEntryCmp(object):
    def __init__(self, feed_id, id):
        self.id = id
        self.feed_id = feed_id

    def __cmp__(self, other):
        return other.id - self.id





@mc_feed_id_list_by_zsite_id("{zsite_id}")
def feed_id_list_by_zsite_id(zsite_id):
    return Feed.where(zsite_id=zsite_id).field_list()


def mc_flush_zsite_follow(zsite_id):
    from follow import follow_cursor
    mc_feed_id_by_for_zsite_follow.delete(zsite_id)
    follow_cursor.execute(
        "select from_id from follow where to_id=%s", zsite_id
    )
    for i, in follow_cursor:
        mc_feed_id_by_for_zsite_follow.delete(i)


mq_mc_flush_zsite_follow = mq_client(mc_flush_zsite_follow)

if __name__ == "__main__":
    mq_mc_flush_zsite_follow(10024787)
