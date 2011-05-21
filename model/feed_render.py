#!/usr/bin/env python
#coding:utf-8


from cid import CID_WORD
from collections import namedtuple

CID2FEED_ENTRY = {
    CID_WORD : ""
}

def __init__cid2feed_entry():
    for k, v in CID2FEED_ENTRY.iteritems():
        CID2FEED_ENTRY[k] = namedtuple(
            'Entry%s'%k,
            " ".join(('id cid feed_id zsite_id',v))
        )

__init__cid2feed_entry()


def load_word(id):
    return ()


CID2LOAD = {
    CID_WORD:load_word
}

def render_feed_entry_list(entry_list):
    result = []
    for id, cid, feed_id, zsite_id in entry_list:
        args = CID2LOAD[cid](id)
        cls = CID2FEED_ENTRY[cid]
        result.append(cls(id, cid, feed_id, zsite_id, *args))
    return result


