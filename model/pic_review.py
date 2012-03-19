#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pic import Pic
from cid import CID_ICO, CID_ICO96


def _pic_list_to_review_by_cid(cid, start_id, limit):
    return Pic.where(cid=cid, state=1, admin_id=0).where('id>%s' % start_id).order_by('id')[:limit]

def pic_ico_to_review_iter(limit):
    from ico import ico
    count = 0
    start_id = 0
    while True:
        li = _pic_list_to_review_by_cid(CID_ICO, start_id, limit)
        for i in li:
            id = i.id
            user_id = i.user_id
            user_pic_id = ico.get(user_id)
            if id == user_pic_id:
                count += 1
                yield i
                if count == limit:
                    return
            else:
                i.state = 0
                i.save()
        if len(li) < limit:
            return
        else:
            start_id = id

def pic_ico_to_review(limit):
    return list(pic_ico_to_review_iter(limit))

def pic_to_review_count_by_cid(cid):
    return Pic.where(cid=cid, state=1, admin_id=0).count()

def pic_list_to_review_by_cid(cid, limit):
    if cid == CID_ICO:
        return pic_ico_to_review(limit)
    return _pic_list_to_review_by_cid(cid, limit)

def pic_list_reviewed_by_cid_state(cid, state, limit, offset):
    return Pic.where(cid=cid, state=state).where('admin_id>0').order_by('id desc')[offset: offset + limit]

def pic_reviewed_count_by_cid_state(cid, state):
    return Pic.where(cid=cid, state=state).where('admin_id>0').count()
