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
    if zsite_show_get(zsite_id, cid):
        return
    zsite_list_new(zsite_id, OWNER_ID, cid, rank)

def zsite_show_rm(zsite):
    zsite_list_rm(zsite.id, OWNER_ID, zsite.cid)

def zsite_show_get(zsite_id, cid=CID_USER):
    return zsite_list_get(zsite_id, OWNER_ID, cid)

def zsite_show_rank(zsite_id, rank):
    zsite_list_rank(zsite_id, OWNER_ID, rank)

SHOW_LIST = (10074584, 10001433, 10054091, 10024555, 10014854, 10061647, 10002480, 10003683, 10007880, 10032093, 10014869, 10000144, 10024889, 10002312, 10003144, 10005102, 10022529, 10009692, 10000895, 10023650, 10006677, 10001875, 10017914, 10004712, 10016542, 10005981, 10055189, 10010156, 10073373, 10015306, 10009186, 10001929, 10010448, 10051930, 10018133, 10066598, 10028737, 10002687, 10029177, 10008285, 10068652, 10014849, 10011065, 10008692, 10000833, 10029871, 10025636, 10000645, 10000053, 10009225, 10002767, 10009040, 10060523, 10024538, 10001565, 10031402, 10000003, 10014236, 10000619, 10021794, 10014495, 10001397, 10003179, 10026510, 10071965, 10011811, 10009308, 10018282, 10055940, 10002178, 10055228, 10016550, 10019718, 10009854, 10016602, 10007895, 10002709)

if __name__ == '__main__':
    zsite_show_new(820,4)
    pass
    print zsite_show_get( 127, CID_SITE )

