#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCacheM
from collections import namedtuple
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from operator import itemgetter
from po import Po
from po_question import answer_count
from follow import follow_id_list_by_from_id
from model.vote import vote_count
from feed import FeedMerge, MAXINT, Feed, mc_feed_tuple, PAGE_LIMIT
from zsite import Zsite
from zkit.txt import cnenoverflow
from zkit.txt2htm import txt_withlink

CIDMAP = {}


FEED_TUPLE_DEFAULT_LEN = 9

def feed_tuple_by_db(id):
    m = Po.mc_get(id)
    cid = m.cid
    rid = m.rid

    if rid:
        question = m.question
        name = question.name
    elif cid != CID_WORD:
        name = m.name
    else:
        name = None

    if cid == CID_QUESTION:
        reply_count = answer_count(id)
    else:
        reply_count = m.reply_count

    result = [
        m.user_id,
        cid,
        rid,
        reply_count,
        m.create_time,
        name,
        vote_count(id)
    ]

    txt = m.txt
    if cid == CID_NOTE or cid == CID_QUESTION or cid == CID_ANSWER:
        result.extend(cnenoverflow(txt, 164))
    else:
        if cid == CID_WORD:
            txt = txt_withlink(txt)
        result.extend((txt, False))

#    if rid:
#        user = question.user
#        result.extend((question.link, user.name, user.link))

    return result

def cidmap(cid):
    def _(cls):
        CIDMAP[cid] = cls
        return cls
    return _

class FeedBase(object):
    def __init__(self, id, rt_id_list, cid, reply_count, zsite_id, vote, name):
        self.id = id
        self.rt_id_list = rt_id_list
        self.cid = cid
        self.reply_count = reply_count
        self.zsite_id = zsite_id
        self.vote = vote
        self.name = name

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

def dump_zsite(zsite):
    if zsite:
        return (zsite.name, zsite.link)
    return (0, 0)

def render_feed_list(id_list, rt_dict):
    zsite_id_list = []

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
        rt_id_list = rt_dict[id]
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
