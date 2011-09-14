#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCacheM
from collections import namedtuple
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_AUDIO, CID_VIDEO, CID_EVENT
from operator import itemgetter
from po import Po
from po_question import answer_count
from follow import follow_id_list_by_from_id
#from vote import vote_count
from feed import FeedMerge, MAXINT, Feed, mc_feed_tuple, PAGE_LIMIT, feed_rm
from zkit.earth import place_name
from zsite import Zsite
from zkit.txt import cnenoverflow
from txt2htm import txt_withlink
from fs import fs_url_jpg, fs_url_audio
from days import begin_end_by_minute
from event import Event
from fav import fav_cid_dict


FEED_TUPLE_DEFAULT_LEN = 12

def feed_tuple_by_db(id):
    m = Po.mc_get(id)
    if not m:
        feed_rm(id)
    cid = m.cid
    rid = m.rid
    has_question = cid in (CID_WORD, CID_ANSWER)

    if rid and has_question:
        question = m.target
        name = question.name
    elif cid != CID_WORD:
        name = m.name
    else:
        name = None

    if cid == CID_QUESTION:
        reply_count = answer_count(id)
    else:
        reply_count = m.reply_count


    if cid == CID_PHOTO:
        _rid = fs_url_jpg(677, rid)
    elif cid == CID_AUDIO:
        _rid = fs_url_audio(id, '')
    elif cid == CID_EVENT:
        event = Event.mc_get(id)
        _rid = fs_url_jpg(162, event.pic_id)
    else:
        _rid = rid

    result = [
        m.user_id,
        cid,
        _rid,
        reply_count,
        m.create_time,
        name,
        #vote_count(id)
    ]

    txt = m.txt
    if cid != CID_WORD:
        txt, has_more = cnenoverflow(txt, 164)
        if not has_more:
            txt = m.htm
        result.extend((txt, has_more))
    else:
        txt = txt_withlink(txt)
        result.extend((txt, False))

    if cid == CID_EVENT:
        result.append(place_name(event.pid))
        result.append(event.address)
        result.extend(
            begin_end_by_minute(event.begin_time, event.end_time)
        )
    elif rid and has_question:
        user = question.user
        result.extend(
            (question.id, user.name, user.link)
        )


    return result


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


def render_feed_list(id_list, rt_dict, zsite_id):
    zsite_id_list = []

    for i in rt_dict.itervalues():
        zsite_id_list.extend(i)

    zsite_dict = Zsite.mc_get_dict(filter(bool, zsite_id_list))
    fav_dict = fav_cid_dict(zsite_id, id_list)
    r = []
    for id, i in zip(id_list, feed_tuple_list(id_list)):
        rt_id_list = rt_dict[id]
        result = [
            i[0],
            id,
            map(dump_zsite, map(zsite_dict.get, rt_id_list)),
            fav_dict[id],
        ]
        result.extend(i[1:])
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
    id = 0
    for i in feed_merge.merge_iter(limit, begin_id):
        rid = i.rid
        id = rid or i.id
        if id not in rt_dict:
            rt_dict[id] = []
            id_list.append(id)
        if rid:
            rt_dict[id].append(i.zsite_id)
    return render_feed_list(id_list, rt_dict, zsite_id), id


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
    m = Po.mc_get(10044641)
    print feed_tuple_by_db(10033928)
    print feed_tuple_list([10033927])
