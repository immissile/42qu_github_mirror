#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zsite_list import ZsiteList, zsite_id_list, zsite_list_new, zsite_list_rm, zsite_list_get, zsite_list_rank, mc_flush_owner_id_cid, zsite_id_list_order_id_desc
from functools import partial
from zsite_rank import zsite_rank_get
from zweb.orm import ormiter
from model.cid import CID_USER, CID_SITE

OWNER_ID = 0

zsite_show = partial(zsite_id_list, 0, 0)
user_list_verify = partial(zsite_id_list_order_id_desc, 0, 0)
#def zsite_show(limit=None, offset=None):
#    return zsite_list(0, 0, limit, offset)

def zsite_show_update():
    for i in ormiter(ZsiteList, 'owner_id=0 and cid=0'):
        i.rank = zsite_rank_get(i.zsite_id)
        i.save()
    mc_flush_owner_id_cid(0, 0)

def zsite_show_new(zsite_id, cid=CID_USER, rank=1):
    cid_list = [] # TODO
    zsite_list_new(zsite_id, cid, cid_list, rank)

def zsite_show_rm(zsite_id):
    zsite_list_rm(zsite_id, 0)

def zsite_show_get(zsite_id):
    return zsite_list_get(zsite_id, 0, 0)

def zsite_show_rank(zsite_id, rank):
    zsite_list_rank(zsite_id, 0, rank)


if __name__ == '__main__':
#    print zsite_show()
    pass
