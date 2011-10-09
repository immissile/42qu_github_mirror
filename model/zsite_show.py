#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zsite_list import ZsiteList, zsite_id_list, zsite_list_new, zsite_list_rm, zsite_list_get, zsite_list_rank, mc_flush, zsite_id_list_order_id_desc, zsite_list_count
from functools import partial
from zsite_rank import zsite_rank_get
from zweb.orm import ormiter
from model.cid import CID_USER, CID_SITE
from model.zsite import Zsite

OWNER_ID = 0

user_show_id_list = partial(zsite_id_list_order_id_desc, OWNER_ID, CID_USER)

def zsite_show_list(cid, limit=None, offset=None):
    id_list = zsite_id_list(OWNER_ID, cid, limit, offset)
    return Zsite.mc_get_list(id_list)

def zsite_show_count(cid):
    return zsite_list_count(OWNER_ID, cid)

def zsite_show_update():
    for i in ormiter(ZsiteList, 'owner_id=0'):
        i.rank = zsite_rank_get(i.zsite_id)
        i.save()

    for cid in (CID_SITE, CID_USER):
        mc_flush(OWNER_ID, cid)

def zsite_show_new(zsite_id, cid, rank=1):
    zsite_list_new(zsite_id, OWNER_ID, cid, rank)

def zsite_show_rm(zsite_id, cid=None):
    zsite_list_rm(zsite_id, OWNER_ID)

def zsite_show_get(zsite_id, cid=CID_USER):
    return zsite_list_get(zsite_id, OWNER_ID, cid)

def zsite_show_rank(zsite_id, rank):
    zsite_list_rank(zsite_id, OWNER_ID, rank)


if __name__ == '__main__':
    pass
    print zsite_show_get( 127, CID_SITE )

