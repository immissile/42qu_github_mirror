#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from zkit.algorithm.merge import imerge
from state import STATE_ACTIVE
from feed import MAXINT, PAGE_LIMIT


mc_feed_po_iter = McCacheA('FeedPoIter.%s')
mc_feed_po_dict = McCache('FeedPoDict.%s')

cursor = cursor_by_table('po')

FEED_PO_ID_LASTEST_SQL = 'select id from po where user_id=%%s and state=%s order by id desc limit %s' % (STATE_ACTIVE, PAGE_LIMIT)
FEED_PO_ID_ITER_SQL = 'select id from po where user_id=%%s and state=%s and id<%%s order by id desc limit %s' % (STATE_ACTIVE, PAGE_LIMIT)

@mc_feed_po_iter('{feed_id}')
def feed_po_id_lastest(feed_id):
    cursor.execute(FEED_PO_ID_LASTEST_SQL, feed_id)
    return [i for i, in cursor.fetchall()]

def feed_po_iter(zsite_id, start_id=None):
    if start_id is None:
        id_list = feed_po_id_lastest(zsite_id)
        if id_list:
            for i in id_list:
                yield i
            start_id = i
        else:
            return
    elif start_id == 0:
        return
    while True:
        cursor.execute(FEED_PO_ID_ITER_SQL, (zsite_id, start_id))
        c = cursor.fetchall()
        if not c:
            break
        for i, in c:
            yield i
        start_id = i


def feed_po_merge_iter(zsite_id_list, limit=PAGE_LIMIT, begin_id=None):
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
