#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_WORD, CID_NOTE
from collections import namedtuple
from zsite import Zsite
from operator import itemgetter
from po import feed_tuple_word, feed_tuple_note
from feed import FeedMerge, MAXINT
from follow import follow_id_list_by_from_id
from model.vote import vote_count

@mc_feed_tuple('{id}')
def feed_tuple_note(id):
    m = Po.mc_get(id)
    if m:
        return (m.name, m.txt, m.reply_total)
    return ()

@mc_feed_tuple('{id}')
def feed_tuple_word(id):
    m = Po.mc_get(id)
    if m:
        return (m.name, m.reply_total)
    return False

CID2FEEDFUNC = {
    CID_WORD: feed_tuple_word,
    CID_NOTE: feed_tuple_note,
}


CID2FEED_ENTRY = {
    CID_WORD: 'txt reply_total',
    CID_NOTE: 'name txt reply_total',
}

def __init__cid2feed_entry():
    for k, v in CID2FEED_ENTRY.iteritems():
        CID2FEED_ENTRY[k] = namedtuple(
            'Entry%s'%k,
            ' '.join(('id vote cid feed_id zsite zsite_id', v))
        )

__init__cid2feed_entry()

def zsite_id_list_by_follow(zsite_id):
    r = follow_id_list_by_from_id(zsite_id)
    r.append(0)
    r.append(zsite_id)
    return r

def render_iter(zsite_id, limit=MAXINT, begin_id=MAXINT):
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

def render_feed_list(id_list, rt_dict):
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


