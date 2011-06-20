#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from time import time
from fs import fs_set_jpg, fs_url_jpg

class Pic(Model):
    def __getattr__(self, name):
        if name.startswith('ico'):
            size = name[3:]
            if size.isdigit():
                return fs_url_jpg(size, self.id)

def pic_new(cid, user_id):
    p = Pic(
        cid=cid,
        user_id=user_id,
        create_time=int(time()),
    ).save()
    return p.id

def pic_save(pic_id, pic):
    fs_set_jpg('0', pic_id, pic)

def pic_need_review(cid):
    qs = Pic.where(cid=cid, admin_id=0)[:1]
    return len(qs)

def pic_list_to_review_by_cid(cid, limit):
    return Pic.where(cid=cid, admin_id=0).order_by('id')[:limit]

def pic_list_reviewed_by_cid_state(cid, state, limit, offset):
    return Pic.where(cid=cid, state=state).where('admin_id>0').order_by('id desc')[offset: offset + limit]
