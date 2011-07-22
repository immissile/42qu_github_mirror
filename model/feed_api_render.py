#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from po import Po
from feed_render import zsite_id_list_by_follow
from feed import MAXINT, PAGE_LIMIT
from feed_po import feed_po_iter, feed_po_merge_iter, mc_feed_po_dict
from zsite import Zsite
from zkit.txt2htm import txt_withlink
from zkit.mc_func import mc_func_get_list

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

    d = dict(id=id, cid=cid, user=user_dict(o.user_id))

    if cid == CID_WORD and rid or cid == CID_ANSWER:
        d.update(question_dict(rid))
    else:
        d['name'] = o.name

    txt = o.txt
    if txt:
        d['txt'] = txt

    return d

def feed_po_dict_list(id_list):
    return mc_func_get_list(mc_feed_po_dict, feed_po_dict_by_db, id_list)

def render_feed_api_by_zsite_id(zsite_id, limit=PAGE_LIMIT, begin_id=None):
    zsite_id_list = zsite_id_list_by_follow(zsite_id)
    id_list = []
    i = 0
    for i in feed_po_merge_iter(zsite_id_list, limit, begin_id):
        id_list.append(i)
    return feed_po_dict_list(id_list), i

def render_user_feed_api_by_zsite_id(zsite_id, limit=PAGE_LIMIT, begin_id=None):
    id_list = []
    i = 0
    count = 0
    for i in feed_po_iter(zsite_id, begin_id):
        id_list.append(i)
        count += 1
        if count >= limit:
            break
    return feed_po_dict_list(id_list), i

if __name__ == '__main__':
    pass
