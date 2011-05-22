#!/usr/bin/env python
#coding:utf-8

from _db import cursor_by_table, Model, McCache, McLimitA, McCacheA, McModel
from zkit.mc_func import mc_func_get_list
from follow import follow_id_list_by_from_id
from zkit.algorithm.merge import imerge
from mq import mq_client
from feed_entry import mc_feed_entry_tuple,MAXINT,feed_entry_cmp_iter
from feed_render import render_feed_entry_list

mc_feed_id_by_zsite_id_cid = McCache("FeedIdByZsiteIdCid:%s")
mc_feed_id_list_by_zsite_id = McCacheA("FeedIdByZsiteId:%s")
mc_feed_id_by_for_zsite_follow = McCacheA("FeedIdForZsiteFollow<%s")


class Feed(McModel):
    pass


@mc_feed_id_list_by_zsite_id("{zsite_id}")
def feed_id_list_by_zsite_id(zsite_id):
    return Feed.where(zsite_id=zsite_id).id_list()

@mc_feed_id_by_for_zsite_follow("{zsite_id}")
def feed_id_list_for_zsite_follow(zsite_id):
    key_list = follow_id_list_by_from_id(zsite_id)
    key_list.append(zsite_id)
    feed_id_list = mc_func_get_list(
        mc_feed_id_list_by_zsite_id,
        feed_id_list_by_zsite_id,
        key_list
    )
    r = set()
    for i in feed_id_list:
        r.update(i)
    return r

def mc_flush_zsite_follow(zsite_id):
    mc_feed_id_by_for_zsite_follow.delete(zsite_id)
    for i in follow_id_list_by_from_id(zsite_id):
        mc_feed_id_by_for_zsite_follow.delete(i)


mq_mc_flush_zsite_follow = mq_client(mc_flush_zsite_follow)


@mc_feed_id_by_zsite_id_cid("{zsite_id}_{cid}")
def feed_id_by_zsite_id_cid(zsite_id, cid):
    feed = Feed.get_or_create(zsite_id=zsite_id, cid=cid)
    if not feed.id:
        feed.save()
        mc_feed_id_list_by_zsite_id.delete(zsite_id)
        mq_mc_flush_zsite_follow(zsite_id)
    return feed.id


class FeedMerge(object):
    def __init__(self, feed_id_list):
        self.feed_id_list = feed_id_list

    def merge_iter(self, limit=MAXINT, begin_id=MAXINT):
        feed_id_list = self.feed_id_list
        count = 0
        for i in imerge(
            *[
                feed_entry_cmp_iter(i, begin_id)
                for i in
                feed_id_list
            ]
        ):
            yield i
            count += 1
            if count >= limit:
                break

    def render_iter(self, limit=MAXINT, begin_id=MAXINT):
        feed_id_set = set()

        r = []
        for i in self.merge_iter(limit, begin_id):
            feed_id_set.add(i.feed_id)
            r.append(i)

        r2 = []
        feed_dict = Feed.mc_get_multi(feed_id_set)
        for i in r:
            feed = feed_dict[i.feed_id]
            cid = feed.cid
            r2.append( ( i.id, cid, i.feed_id, feed.zsite_id ) )
        return render_feed_entry_list(r2)

def feed_render_iter_for_zsite_follow(zsite_id, limit=MAXINT, begin_id=MAXINT):
    feed_id_list = feed_id_list_for_zsite_follow(zsite_id)
    return FeedMerge(feed_id_list).render_iter(limit, begin_id)

if __name__ == "__main__":
    pass
   # from cid import CID_WORD
   # for i in feed_render_iter_for_zsite_follow( 10024772 ):
   #     print i.cid
