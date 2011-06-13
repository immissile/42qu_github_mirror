#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCacheM
from collections import namedtuple
from cid import CID_WORD, CID_NOTE
from operator import itemgetter
from po import Po
from follow import follow_id_list_by_from_id
from model.vote import vote_count
from feed import FeedMerge, MAXINT, Feed, mc_feed_tuple, PAGE_LIMIT
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
        self.vote = vote
        self.name = name

def feed_tuple_by_db(id):
    m = Po.mc_get(id)
    cid = m.cid
    result = [m.user_id, cid, m.reply_total, m.name, vote_count(id)]
    if cid == CID_NOTE:
        result.append(m.txt)
    return result

def feed_tuple_list(id_list):
    r = mc_feed_tuple.get_dict(id_list)
    k = []

    for i in id_list:
        result = r[i]
        if result is None:
            result = feed_tuple_by_db(i)
            mc_feed_tuple.set(i, result)
        k.append(result)

    return k

#note = zsite_id, cid, reply_total, vote, name, txt
#word = zsite_id, cid, reply_total, vote, name
def dump_zsite(zsite):
    if zsite:
        return (zsite.name, zsite.link)
    return (0, 0)

def render_feed_list(id_list, rt_dict):
    zsite_id_list = []
    print rt_dict
    for i in rt_dict.itervalues():
        zsite_id_list.extend(i)
    for id, i in zip(id_list, feed_tuple_list(id_list)):
        zsite_id = i[0]
        zsite_id_list.append(zsite_id)

        rt_id_list = rt_dict[id]
        zsite_id_list.extend(rt_id_list)

    zsite_dict = Zsite.mc_get_dict(filter(bool, zsite_id_list))
    r = []
    for id, i in zip(id_list, feed_tuple_list(id_list)):
        zsite_id = i[0]
        zsite = zsite_dict[zsite_id]
        result = [
            id,
            dump_zsite(zsite),
            map(dump_zsite, map(zsite_dict.get, rt_id_list))
        ]
        result.extend(i)
        r.append(result)
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
        if id not in rt_dict:
            rt_dict[id] = []
            id_list.append(id)
        if rid:
            rt_dict[id].append(i.zsite_id)

    return render_feed_list(id_list, rt_dict)


#    result = []
#    zsite_dict = Zsite.mc_get_dict(set(map(itemgetter(3), entry_list)))
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


