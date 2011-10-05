#coding:utf-8
from _db import McModel, McCache, cursor_by_table, McCacheA, McCacheM
from feed import PAGE_LIMIT, cursor

FEED_ID_LASTEST_SQL = 'select id, rid from feed where zsite_id=%%s order by id desc limit %s'%PAGE_LIMIT
FEED_ID_ITER_SQL = 'select id, rid from feed where zsite_id=%%s and id<%%s order by id desc limit %s'%PAGE_LIMIT

mc_site_feed_iter = McCacheM('SiteFeedIter:%s')

#@mc_site_feed_iter('{feed_id}')
def site_feed_id_lastest(feed_id):
    cursor.execute(FEED_ID_LASTEST_SQL, feed_id)
    return tuple(cursor.fetchall())


if __name__ == '__main__':
    from model.state import STATE_PO_ZSITE_SHOW_THEN_REVIEW
    from model.po import Po
    c = Po.where(
        zsite_id=10099440
    ).where('state>=%s'%STATE_PO_ZSITE_SHOW_THEN_REVIEW)
    print c.col_list()

