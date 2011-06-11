#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from mq import mq_client

MAXINT = sys.maxint 
PAGE_LIMIT = 42
FEED_ID_LASTEST_SQL = 'select id, rid from feed where zsite_id=%%s order by id desc limit %s'%PAGE_LIMIT
FEED_ID_ITER_SQL = 'select id, rid from feed where zsite_id=%%s and id<%%s order by id desc limit %s'%PAGE_LIMIT

mc_feed_tuple = McCacheM('FeedTuple:%s')
mc_feed_iter = McCacheM('FeedIter:%s')

cursor = cursor_by_table('feed')

def feed_new(id, zsite_id, cid, rid=0):
    cursor.execute(
        'insert into feed (id, zsite_id, cid, rid) values (%s,%s,%s,%s) on duplicate key update id=id',
        (id, zsite_id, cid, rid)
    )
    cursor.connection.commit()
    mc_feed_iter.delete(zsite_id)
    return id

def feed_rm(id):
    cursor.execute('select zsite_id from feed where id=%s', id)
    r = cursor.fetchone()
    if r:
        zsite_id = r[0]
        cursor.execute('delete from feed where id=%s', id)
        cursor.connection.commit()
        mc_feed_iter.delete(zsite_id)
    feed_rm_rt(id)
    #TODO MQ
    #mq_feed_rm_rt(id)


def feed_rm_rt(rid):
    cursor.execute('select id, zsite_id from feed where rid=%s', rid)
    for id, zsite_id in cursor:
        cursor.execute('delete from feed where id=%s', id)
        cursor.connection.commit()
        mc_feed_iter.delete(zsite_id)

mq_feed_rm_rt = mq_client(feed_rm_rt)

@mc_feed_iter('{feed_id}')
def feed_id_lastest(feed_id):
    cursor.execute(FEED_ID_LASTEST_SQL, feed_id)
    return tuple(cursor.fetchall())

#TODO : 消息流的合并, feed_entry_id_iter 函数可以考虑用天涯的内存数据库来优化
#http://code.google.com/p/memlink/
def feed_iter(zsite_id, start_id=MAXINT):
    if start_id == MAXINT:
        id_list = feed_id_lastest(id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i
        else:
            return
    while True:
        cursor.execute(FEED_ID_ITER_SQL, (id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i, in c:
            yield i
        start_id = i


def feed_cmp_iter(zsite_id, start_id=MAXINT):
    for id, rid in feed_iter(zsite_id, start_id):
        yield FeedEntryCmp(id, rid, zsite_id)

class FeedCmp(object):
    def __init__(self, id, rid, zsite_id):
        self.id = id
        self.rid = rid
        self.zsite_id = zsite_id

    def __cmp__(self, other):
        return other.id - self.id


if __name__ == '__main__':
    pass
