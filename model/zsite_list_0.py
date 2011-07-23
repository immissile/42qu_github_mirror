#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zsite_list import ZsiteList, zsite_id_list, zsite_list_new, zsite_list_rm, zsite_list_get, zsite_list_rank, mc_flush_owner_id_cid, zsite_id_list_reverse
from functools import partial
from zsite_rank import zsite_rank_get
from zweb.orm import ormiter

OWNER_ID = 0

zsite_show = partial(zsite_id_list, 0, 0)
user_list_verify = partial(zsite_id_list_reverse, 0, 0)
#def zsite_show(limit=None, offset=None):
#    return zsite_list(0, 0, limit, offset)

def zsite_show_update():
    for i in ormiter(ZsiteList, 'owner_id=0 and cid=0'):
        i.rank = zsite_rank_get(i.zsite_id)
        i.save()
    mc_flush_owner_id_cid(0, 0)

def zsite_show_new(zsite_id, rank=1000):
    cid_list = [] # TODO
    zsite_list_new(zsite_id, 0, cid_list, rank)

def zsite_show_rm(zsite_id):
    zsite_list_rm(zsite_id, 0)

def zsite_show_get(zsite_id):
    return zsite_list_get(zsite_id, 0, 0)

def zsite_show_rank(zsite_id, rank):
    zsite_list_rank(zsite_id, 0, rank)


if __name__ == '__main__':
#    print zsite_show()
    zsite_show_update()
    from model.zsite import Zsite
    for i in ormiter(ZsiteList, 'owner_id=0 and cid=0'):
        if i.rank:
            print i.zsite_id
            print i.rank
