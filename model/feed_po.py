#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from zkit.algorithm.merge import imerge
from state import STATE_ACTIVE
from feed import MAXINT, PAGE_LIMIT


mc_feed_po_iter = McCacheA('FeedPoIter.%s')
mc_feed_po_json = McCache('FeedPoJson.%s')

cursor = cursor_by_table('po')

FEED_PO_ID_LASTEST_SQL = 'select id from po where user_id=%%s and state=%s order by id desc limit %s' % (STATE_ACTIVE, PAGE_LIMIT)
FEED_PO_ID_ITER_SQL = 'select id from po where user_id=%%s and state=%s and id<%%s order by id desc limit %s' % (STATE_ACTIVE, PAGE_LIMIT)

@mc_feed_po_iter('{feed_id}')
def feed_po_id_lastest(feed_id):
    cursor.execute(FEED_PO_ID_LASTEST_SQL, feed_id)
    return [i for i, in cursor.fetchall()]

def feed_po_iter(zsite_id, start_id=MAXINT):
    if start_id == MAXINT:
        id_list = feed_po_id_lastest(zsite_id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i
        else:
            return
    while True:
        cursor.execute(FEED_PO_ID_ITER_SQL, (zsite_id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i, in c:
            yield i
        start_id = i


class FeedPoMerge(object):
    def __init__(self, zsite_id_list):
        self.zsite_id_list = zsite_id_list

    def merge_iter(self, limit=MAXINT, begin_id=MAXINT):
        zsite_id_list = self.zsite_id_list
        count = 0
        for i in imerge(
            *[
                feed_po_iter(i, begin_id)
                for i in
                zsite_id_list
            ]
        ):
            yield i
            count += 1
            if count >= limit:
                break


if __name__ == '__main__':
    pass
