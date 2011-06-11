#!/usr/bin/env python
# -*- coding: utf-8 -*-
from feed import mc_feed_tuple, MAXINT, feed_cmp_iter
from feed_render import render_feed_entry_list
from zkit.mc_func import mc_func_get_list
from zkit.algorithm.merge import imerge
from follow import follow_id_list_by_from_id

class FeedMerge(object):
    def __init__(self, zsite_id_list):
        self.zsite_id_list = zsite_id_list

    def merge_iter(self, limit=MAXINT, begin_id=MAXINT):
        zsite_id_list = self.zsite_id_list
        count = 0
        for i in imerge(
            *[
                feed_cmp_iter(i, begin_id)
                for i in
                zsite_id_list
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

        for i in zip(r):
            r2.append( (i.id, i.zsite_id) )

        return render_feed_entry_list(r2)

def zsite_id_list_by_follow(zsite_id):
    r = follow_id_list_by_from_id(zsite_id)
    r.append(0)
    r.append(zsite_id)
    return r

def feed_render_iter_by_follow(zsite_id, limit=MAXINT, begin_id=MAXINT):
    zsite_id_list = zsite_id_list_by_follow(zsite_id)
    return FeedMerge(zsite_id_list).render_iter(limit, begin_id)

if __name__ == '__main__':
    pass

