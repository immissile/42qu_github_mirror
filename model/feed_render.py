#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from _db import McCacheM
from collections import namedtuple
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_AUDIO, CID_VIDEO, CID_EVENT, CID_USER, CID_REC
from operator import itemgetter
from po import Po
from po_question import answer_count
from follow import follow_id_list_by_from_id
#from vote import vote_count
from feed import feed_merge_iter, MAXINT, Feed, mc_feed_tuple, PAGE_LIMIT, feed_rm
from zkit.earth import place_name
from zsite import Zsite
from zkit.txt import cnenoverflow
from txt2htm import txt_withlink
from fs import fs_url_jpg, fs_url_audio
from model.career import career_dict
from days import begin_end_by_minute
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from event import Event
from fav import fav_cid_dict
from zkit.ordereddict import OrderedDict
from model.po_video import video_link_autoplay

FEED_TUPLE_DEFAULT_LEN = 12

FEED_TUPLE_DEFAULT_LEN_FOR_ZSITE = 10

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
    elif cid == CID_REC:
        name = m.name_htm
    elif cid != CID_WORD:
        name = m.name
    else:
        name = None

    #if cid == CID_QUESTION:
    #    reply_count = answer_count(id)
    #else:
    reply_count = m.reply_count
    if cid == CID_PHOTO:
        rid = fs_url_jpg(721, rid)
    elif cid == CID_AUDIO:
        rid = fs_url_audio(id, '')
    elif cid == CID_VIDEO:
        rid = video_link_autoplay(cid, rid)
    elif cid == CID_EVENT:
        event = Event.mc_get(id)
        feed_rm(id)
        rid = fs_url_jpg(162, event.pic_id)
    else:
        rid = rid

    result = [
        m.user_id,
        cid,
        rid,
        m.zsite_id,
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
        return (zsite.name, zsite.link, zsite.id)
    return (0, 0)


def render_feed_list(id_list, zsite_id, rt_dict) :
    fav_dict = fav_cid_dict(zsite_id, id_list)
    r = []
    for id, i in zip(id_list, feed_tuple_list(id_list)):
        out = []
        if id in rt_dict:
            for  v in rt_dict[id]:
                entry = []
                if v[2]>0:
                    zsite = Zsite.mc_get(v[2])
                    _name = zsite.name
                    _link = zsite.link
                    _user_id = v[2]
                else:
                    _name = '1'
                    _link = '1'
                    _user_id = v[2]

                entry.extend([_name,_link, _user_id,v])
                out.append(entry)

        result = [
            i[0],
            id,
            out,
            fav_dict[id],
        ]
        result.extend(i[1:])

        r.append(result)

    return r

def render_zsite_feed_list(user_id, id_list):
    fav_dict = fav_cid_dict(user_id, id_list)
    r = []
    rf = feed_tuple_list(id_list)

    zsite_id_set = set(
        i[0] for i in rf
    )
    z_dict = Zsite.mc_get_dict(zsite_id_set)
    c_dict = career_dict(id for id, i in z_dict.iteritems() if i.cid == CID_USER)
    z_dict = dict(
        (i.id, (i.name, i.link))
        for i in z_dict.itervalues()
    )

    for id, i in zip(id_list, rf):
        zsite_id = i[0]
        cid = i[1]

        result = [
            zsite_id,
            id,
            fav_dict[id],
        ]
        if cid not in (CID_WORD, CID_EVENT):
            result.extend(i[1:9])
            result.extend(zsite_tag_id_tag_name_by_po_id(zsite_id, id))
            if len(i) > 9:
                result.extend(i[9:])
        else:
            result.extend(i[1:])

        r.append(result)

    return r, z_dict, c_dict

def zsite_id_list_by_follow(zsite_id):
    r = follow_id_list_by_from_id(zsite_id)
    r.append(0)
    r.append(zsite_id)
    return r

def render_feed_by_zsite_id(zsite_id, limit=MAXINT, begin_id=MAXINT):
    zsite_id_list = zsite_id_list_by_follow(zsite_id)
    rt_dict = defaultdict(list)

    id_list = []
    id = 0
    for i in feed_merge_iter(zsite_id_list, limit, begin_id):
        id = i.id
        po = Po.mc_get(id)
        if po is None:
            continue
        if po.cid == CID_REC:
            id = po.rid
            od = rt_dict[id]
            user_id = po.user_id
            data = (po.id, po.txt,po.user_id)
            od.append(data)
        else:
            id = po.id

        if id not in id_list:
            id_list.append(id)


    return render_feed_list(id_list, zsite_id, rt_dict), id


if __name__ == '__main__':
    feed_rm(10187807)
    for i in render_feed_by_zsite_id(10071241, 100):
        pass
