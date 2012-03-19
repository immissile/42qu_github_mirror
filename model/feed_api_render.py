#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_WORD, CID_ANSWER
from po import Po
from feed_render import zsite_id_list_by_follow
from feed import PAGE_LIMIT
from feed_po import feed_po_iter, FeedPoMerge, mc_feed_po_dict, mc_feed_user_dict
from zsite import Zsite
from zkit.mc_func import mc_func_get_list, mc_func_get_dict
from txt import txt_get

@mc_feed_user_dict('{user_id}')
def user_dict(user_id):
    user = Zsite.mc_get(user_id)
    unit, title = user.career
    d = dict(id=user_id, name=user.name, unit=unit, title=title)
    ico_url = user._ico96
    if ico_url:
        d['ico_url'] = ico_url
    return d

def question_dict(question_id):
    o = Po.mc_get(question_id)
    return dict(question_id=question_id, question_name=o.name, question_user=user_dict(o.user_id))

def feed_po_dict_by_db(id):
    o = Po.mc_get(id)
    cid = o.cid
    rid = o.rid

    d = dict(id=id, cid=cid)

    if cid == CID_WORD and rid or cid == CID_ANSWER:
        d.update(question_dict(rid))
    else:
        d['name'] = o.name

    return d

def feed_po_dict_list(id_list):
    return mc_func_get_list(mc_feed_po_dict, feed_po_dict_by_db, id_list)

def feed_user_dict_dict(id_list):
    id_list = set(id_list)
    return mc_func_get_dict(mc_feed_user_dict, user_dict, id_list)

def render_feed_api_by_zsite_id(zsite_id, limit=PAGE_LIMIT, begin_id=None):
    feed_merge = FeedPoMerge(zsite_id_list_by_follow(zsite_id))
    id_list = []
    zsite_id_list = []
    id = 0
    for i in feed_merge.merge_iter(limit, begin_id):
        id = i.id
        zsite_id = i.zsite_id
        id_list.append(id)
        zsite_id_list.append(zsite_id)
    user_dict_dict = feed_user_dict_dict(zsite_id_list)
    li = feed_po_dict_list(id_list)
    for i, zsite_id in zip(li, zsite_id_list):
        i['user'] = user_dict_dict[zsite_id]
        txt = txt_get(i['id'])
        if txt:
            i['txt'] = txt
    return li, id

def render_user_feed_api_by_zsite_id(zsite_id, limit=PAGE_LIMIT, begin_id=None):
    id_list = []
    id = 0
    count = 0
    for id in feed_po_iter(zsite_id, begin_id):
        id_list.append(id)
        count += 1
        if count >= limit:
            break
    li = feed_po_dict_list(id_list)
    for i in li:
        txt = txt_get(i['id'])
        if txt:
            i['txt'] = txt
    return li, id

if __name__ == '__main__':
    pass
