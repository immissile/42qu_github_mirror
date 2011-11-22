#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from cid import CID_PRODUCT, CID_COM
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from spammer import is_same_post
from po import Po, po_rm, po_new
import json
from zsite_show import zsite_show_list
from itertools import  chain
from txt import txt_new, txt_get, txt_property


mc_product_id_list_by_com_id = McCacheA("ProductIdListByComId:%s") 

def po_product_new(user_id, name, _info_json, zsite_id=0, state=STATE_ACTIVE):
    if not name and not _info_json :
        return
    info_json = json.dumps(dict(iter(_info_json)))
    if not is_same_post(user_id, name, info_json, zsite_id):
        m = po_new(CID_PRODUCT, user_id, name, state, 0, None, zsite_id)
        txt_new(m.id, info_json)
        mc_product_id_list_by_com_id.delete(zsite_id)
        return m

def po_product_update(po_id, _info_json):
    po = Po.mc_get(po_id)
    if po:
        info_json = json.dumps(dict(iter(_info_json)))
        po.txt_set(info_json)
        po.save()

@mc_product_id_list_by_com_id("{id}")
def product_id_list_by_com_id(id):
    return Po.where(zsite_id=id, cid=CID_PRODUCT, state=STATE_ACTIVE).col_list(col='id')

def product_list_by_com_id(com_id):
    return Po.mc_get_list(product_id_list_by_com_id(com_id))

def product_show_list():
    com_list = zsite_show_list(CID_COM)
    if com_list:
        com_id_list = [c.id for c in com_list]
        if com_id_list:
            return chain.from_iterable(
                [product_list_by_com_id(c) for c in com_id_list]
            )

def product_rm(user_id, id):
    po_rm(user_id, id)
    mc_product_id_list_by_com_id.delete(zsite_id)

