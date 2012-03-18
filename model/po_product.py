#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from cid import CID_PRODUCT, CID_COM, CID_PRODUCT_PIC
from state import STATE_RM, STATE_SECRET, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from spammer import is_same_post
from po import Po, _po_rm, po_new, po_id_list, po_list_count, po_view_list
import json
from zsite_show import zsite_show_list
from itertools import  chain
from txt import txt_new, txt_get, txt_property
from pic import pic_new, pic_save, PicMixin
from fs import fs_set_jpg, fs_url_jpg
from zkit.pic import pic_fit_width_cut_height_if_large


mc_product_id_list_by_com_id = McCacheA('ProductIdListByComId:%s')

def po_product_new(user_id, name, _info_json, zsite_id=0, state=STATE_ACTIVE):
    if not name and not _info_json :
        return
    info_json = json.dumps(dict(iter(_info_json)))
    if not is_same_post(user_id, name, info_json, zsite_id):
        m = po_new(CID_PRODUCT, user_id, name, state, 0, None, zsite_id)
        if m:
            txt_new(m.id, info_json)
            mc_product_id_list_by_com_id.delete(zsite_id)
            return m

def po_product_update(po_id, _info_json):
    po = Po.mc_get(po_id)
    if po:
        info_json = json.dumps(dict(iter(_info_json)))
        po.txt_set(info_json)
        po.save()

@mc_product_id_list_by_com_id('{id}')
def product_id_list_by_com_id(id):
    return Po.where(zsite_id=id, cid=CID_PRODUCT, state=STATE_ACTIVE).col_list(col='id')

def product_list_by_com_id(com_id):
    return Po.mc_get_list(product_id_list_by_com_id(com_id))


def product_rm(com_id , user_id, id):
    po = Po.mc_get(id)
    if po and po.zsite_id == com_id and po.cid == CID_PRODUCT:
        _po_rm(user_id, po)
        mc_product_id_list_by_com_id.delete(com_id)
        from model.po_product_show import product_show_rm
        product_show_rm(po)

def product_pic_new(com_id, product_id, pic):
    pic_id = pic_new(CID_PRODUCT_PIC, com_id)
    pic_save(pic_id, pic)

    p1 = pic_fit_width_cut_height_if_large(pic, 548)
    fs_set_jpg('548', pic_id, p1)

    p2 = pic_fit_width_cut_height_if_large(pic, 215)
    fs_set_jpg('215', pic_id, p2)
    return pic_id


def product_id_list(limit, offset):
    return po_id_list(None, CID_PRODUCT, False, limit, offset)

def product_count():
    return po_list_count(None, CID_PRODUCT, False)

def product_list(limit, offset):
    return po_view_list(None, CID_PRODUCT, False, limit, offset)

if __name__ == '__main__':

    print product_id_list(100, 0)
    print product_count()

