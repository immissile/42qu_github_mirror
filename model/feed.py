#!/usr/bin/env python
# -*- coding: utf-8 -*-

from state import STATE_RM, STATE_ACTIVE
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from mq import mq_client
from zkit.feed_merge import MAXINT, merge_iter as _merge_iter
from cid import CID_REC

PAGE_LIMIT = 50

mc_feed_iter = McCacheM('FeedIter:%s')
mc_feed_tuple = McCacheM('F%s')
mc_feed_rt_id = McCache('R%s')

cursor = cursor_by_table('feed')

 
class Feed(McModel):
    pass

def feed_new(id, zsite_id, cid, rid=0):
    cursor.execute(
        'insert into feed (id, zsite_id, cid) values (%s,%s,%s) on duplicate key update id=id',
        (id, zsite_id, cid)
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


def feed_rt_rm_by_rid(rid):
    cursor.execute('select id, zsite_id from feed where rid=%s', rid)
    for id, zsite_id in cursor:
        cursor.execute('delete from feed where id=%s', id)
        cursor.connection.commit()
        mc_feed_iter.delete(zsite_id)

mq_feed_rt_rm_by_rid = mq_client(feed_rt_rm_by_rid)

def feed_rt_rm(zsite_id, rid):
    ids = feed_rt_id_list(zsite_id, rid)
    if ids:
        for id in ids:
            _id = id[0]
            cursor.execute('delete from feed where id=%s', _id)
            from po import po_rm
            po_rm(zsite_id,_id)
            cursor.connection.commit()
            mc_feed_iter.delete(zsite_id)
            mc_feed_rt_id.delete('%s_%s'%(zsite_id, rid))

def feed_rt(zsite_id, rid):
    feed = Feed.mc_get(rid)
    if feed and not feed.cid==CID_REC and not feed_rt_id(zsite_id, rid):
        from po_recommend import po_recommend_new
        po_recommend_new(rid,zsite_id,'')
        #feed_new(gid(), zsite_id, feed.cid, rid)
        mc_feed_rt_id.delete('%s_%s'%(zsite_id, rid))

def feed_rt_list(zsite_id, limit, offset):
    return Feed.where(zsite_id=zsite_id).where('cid = 73').order_by('id desc').col_list(
        limit, offset, 'id'
    )

def feed_rt_count(zsite_id):
    return Feed.where(zsite_id=zsite_id).where('cid = 73').count()


def feed_rt_id_list(zsite_id, rid):
    cursor.execute(
        'select id from po where user_id=%s and rid=%s and state = %s',
        (zsite_id, rid, STATE_ACTIVE )
    )
    result = cursor.fetchall()
    if result:
        return result
    return 0

@mc_feed_rt_id('{zsite_id}_{rid}')
def feed_rt_id(zsite_id, rid):
    cursor.execute(
        'select po.id from po JOIN feed on po.id=feed.id where po.user_id=%s and po.rid=%s',
        (zsite_id, rid)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0

FEED_ID_LASTEST_SQL = 'select id from feed where zsite_id=%%s order by id desc limit %s'%PAGE_LIMIT
FEED_ID_ITER_SQL = 'select id from feed where zsite_id=%%s and id<%%s order by id desc limit %s'%PAGE_LIMIT

@mc_feed_iter('{feed_id}')
def feed_id_lastest(feed_id):
    cursor.execute(FEED_ID_LASTEST_SQL, feed_id)
    return tuple(cursor.fetchall())

#TODO : 消息流的合并, feed_entry_id_iter 函数可以考虑用天涯的内存数据库来优化
#http://code.google.com/p/memlink/
def feed_iter(zsite_id, start_id=MAXINT):
    if start_id == MAXINT:
        id_list = feed_id_lastest(zsite_id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i[0]
        else:
            return
    while True:
        cursor.execute(FEED_ID_ITER_SQL, (zsite_id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i in c:
            yield i
        start_id = i[0]

def feed_cmp_iter(zsite_id, start_id=MAXINT):
    for id in feed_iter(zsite_id, start_id):
        yield FeedCmp(id[0], 0, zsite_id)

class FeedCmp(object):
    def __init__(self, id, rid, zsite_id):
        self.id = id
        self.rid = rid
        self.zsite_id = zsite_id

    def __cmp__(self, other):
        return  self.id - other.id


def feed_merge_iter(
    id_list, limit=MAXINT, begin_id=MAXINT
):
    return _merge_iter(
        feed_cmp_iter, id_list, limit, begin_id
    )


if __name__ == '__main__':
    pass

    #id = 10204513 
    #feed_rm(id)
