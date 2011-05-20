#!/usr/bin/env python
#coding:utf-8

from _db import cursor_by_table, Model, McCache, McLimitA, McCacheA

mc_id_by_feed_id = McLimitA("IdByFeedId:%s", 128)
mc_feed_id_by_zsite_id_cid = McCache("FeedIdByZsiteIdCid:%s")
mc_feed_id_list_by_zsite_id = McCacheA("FeedIdByZsiteId:%s")

class Feed(Model):
    pass

cursor = cursor_by_table('feed_entry')

def feed_entry_new(id, zsite_id, cid):
    feed_id = feed_id_by_zsite_id_cid(zsite_id, cid)
    cursor.execute(
        "insert into feed_entry (id, feed_id) values (%s,%s)",
        (id, feed_id)
    )
    cursor.connection.commit()
    mc_id_by_feed_id.delete(feed_id)
    return id


@mc_feed_id_by_zsite_id_cid("{zsite_id}_{cid}")
def feed_id_by_zsite_id_cid(zsite_id, cid):
    feed = Feed.get_or_create(zsite_id=zsite_id, cid=cid)
    if not feed.id:
        feed.save()
        mc_feed_id_list_by_zsite_id.delete(zsite_id)
    return feed.id

@mc_id_by_feed_id("{feed_id}")
def id_by_feed_id(feed_id, limit, offset):
    cursor.execute(
        "select id from feed_entry where feed_id=%s order by id desc limit %s offset %s",
        (feed_id, limit, offset)
    )
    return [
        i for i, in cursor
    ]

@mc_feed_id_list_by_zsite_id("{zsite_id}")
def feed_id_list_by_zsite_id(zsite_id):
    return Feed.where(zsite_id=zsite_id).id_list()



if __name__ == "__main__":
    print feed_id_list_by_zsite_id(1)

