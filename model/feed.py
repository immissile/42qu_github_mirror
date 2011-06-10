#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from mq import mq_client

MAXINT = sys.maxint
PAGE_LIMIT = 42
FEED_ENTRY_ID_LASTEST_SQL = 'select id from feed_entry where zsite_id=%%s order by id desc limit %s'%PAGE_LIMIT
FEED_ENTRY_ID_ITER_SQL = 'select id from feed_entry where zsite_id=%%s and id<%%s order by id desc limit %s'%PAGE_LIMIT

mc_feed_entry_tuple = McCacheM('FeedEntryTuple:%s')
mc_feed_entry_iter = McCacheA('FeedEntryIter:%s')

cursor = cursor_by_table('feed_entry')

def feed_entry_new(id, zsite_id, cid, rid=0):
    cursor.execute(
        'insert into feed_entry (id, zsite_id, cid, rid) values (%s,%s,%s,%s) on duplicate key update id=id',
        (id, zsite_id, cid, rid)
    )
    cursor.connection.commit()
    mc_feed_entry_iter.delete(zsite_id)
    return id

def feed_entry_rm(id):
    cursor.execute('select zsite_id from feed_entry where id=%s', id)
    r = cursor.fetchone()
    if r:
        zsite_id = r[0]
        cursor.execute('delete from feed_entry where id=%s', id)
        cursor.connection.commit()
        mc_feed_entry_iter.delete(zsite_id)
    feed_entry_rm_rt(id)
    #TODO MQ
    #mq_feed_entry_rm_rt(id)


def feed_entry_rm_rt(rid):
    cursor.execute('select id, zsite_id from feed_entry where rid=%s', rid)
    for id, zsite_id in cursor:
        cursor.execute('delete from feed_entry where id=%s', id)
        cursor.connection.commit()
        mc_feed_entry_iter.delete(zsite_id)

mq_feed_entry_rm_rt = mq_client(feed_entry_rm_rt)

@mc_feed_entry_iter('{feed_id}')
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







if __name__ == '__main__':
    pass
