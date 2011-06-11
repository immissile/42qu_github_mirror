#!/usr/bin/env python
# -*- coding: utf-8 -*-
from feed import mc_feed_tuple, MAXINT, feed_cmp_iter
from feed_render import render_feed_list
from zkit.mc_func import mc_func_get_list
from zkit.algorithm.merge import imerge
from follow import follow_id_list_by_from_id
from collections import defaultdict

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
        rt = {}
        id_list = []

        for i in self.merge_iter(limit, begin_id):
            rid = i.rid
            id = rid or i.id
            if id not in rt:
                rt[id] = []
                id_list.append(id)
            if rid:
                rt[id].append(i.zsite_id)
             
        return render_feed_list(id_list, rt)

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

