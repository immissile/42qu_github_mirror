#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCacheM
from collections import namedtuple
from cid import CID_WORD, CID_NOTE
from operator import itemgetter
from po import Po
from follow import follow_id_list_by_from_id
from model.vote import vote_count
from feed import FeedMerge, MAXINT, Feed, mc_feed_tuple
from zsite import Zsite

CIDMAP = {}

def cidmap(cid):
    def _(cls):
        CIDMAP[cid] = cls
        return cls
    return _

class FeedBase(object):
    def __init__(self, id, rt_id_list, cid, reply_total, zsite_id, vote, name):
        self.id = id
        self.rt_id_list = rt_id_list
        self.cid = cid
        self.reply_total = reply_total
        self.zsite_id = zsite_id
        self.name = name

@cidmap(CID_NOTE)
class FeedNote(FeedBase):
    pass

@cidmap(CID_WORD)
class FeedWord(FeedBase):
    def __init__(self, id, rt_id_list, cid, reply_total, zsite_id, vote, name, txt):
        FeedBase.__init__(self, id, rt_id_list, cid, reply_total, zsite_id, vote, name)
        self.txt = txt

def feed_tuple_by_db(id):
    m = Po.mc_get(id)
    cid = m.cid
    result = [cid, m.reply_total, m.user_id, vote_count(id)]
    if cid == CID_WORD:
        result.append(m.name)
    elif cid == CID_NOTE:
        result.append(m.name, m.txt)


def feed_tuple_list(id_list):
    r = mc_feed_tuple.get_multi(id_list)
    k = []

    for i in id_list:
        result = r[i]
        if result is None:
            result = feed_render_by_db(i)
            mc_feed_tuple.set(id, result)
        k.append(result)

    return k

def feed_bind(feed_list):
    Zsite.mc_bind(feed_list,"zsite", "zsite_id")

def render_feed_list(id_list, rt_dict):
    r = []
    for id, i in zip(id_list, feed_tuple_list(id_list)):
        cid = i[0]
        c = CIDMAP[cid](id, rt_dict[id], *i)
        r.append(c)
    feed_bind(r)    
    return r

def zsite_id_list_by_follow(zsite_id):
    r = follow_id_list_by_from_id(zsite_id)
    r.append(0)
    r.append(zsite_id)
    return r

def render_feed_by_zsite_id(zsite_id, limit=MAXINT, begin_id=MAXINT):
    feed_merge = FeedMerge(zsite_id_list_by_follow(zsite_id))
    rt_dict = {}
    id_list = []

    for i in feed_merge.merge_iter(limit, begin_id):
        rid = i.rid
        id = rid or i.id
        if id not in rt:
            rt[id] = []
            id_list.append(id)
        if rid:
            rt_dict[id].append(i.zsite_id)

    return render_feed_list(id_list, rt_dict)


#    result = []
#    zsite_dict = Zsite.mc_get_multi(set(map(itemgetter(3), entry_list)))
#    vote_count_list = vote_count.get_list(map(itemgetter(0), entry_list))
#    for (id, cid, feed_id, zsite_id), vote in zip(entry_list, vote_count_list):
#        args = CID2FEEDFUNC[cid](id)
#        if not args:
#            continue
#        cls = CID2FEED_ENTRY[cid]
#        result.append(
#            cls(id, vote, cid, feed_id, zsite_dict[zsite_id], zsite_id, *args)
#        )
#    return result

if __name__ == '__main__':
    pass


