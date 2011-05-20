#!/usr/bin/env python
#coding:utf-8

from _db import cursor_by_table, Model, McCache

mc_feed_id_by_zsite_id_cid = McCache("FeedIdByZsiteIdCid:%s")

class Feed(Model):
    pass

cursor = cursor_by_table('feed')

def feed_entry_new(id, zsite_id, cid):
    feed_id = feed_id_by_zsite_id_cid(zsite_id, cid)
    cursor.execute(
        "insert into feed_entry (id, feed_id) values"
    )


@mc_feed_id_by_zsite_id_cid("{zsite_id}_{cid}")
def feed_id_by_zsite_id_cid(zsite_id, cid):
    feed = Feed.get_or_create(zsite_id=zsite_id, cid=cid)
    if not feed.id:
        feed.save()
    return feed.id
