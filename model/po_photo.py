#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from cgi import escape
from zkit.pic import pic_fit_width_cut_height_if_large
from pic import pic_new, pic_save, PicMixin
from cid import CID_PO_PHOTO
from fs import fs_set_jpg, fs_url_jpg
from po_pic import PoPic
from zsite_tag import po_id_list_by_zsite_tag_id, ZsiteTagPo

PIC_SIZE = 721

def photo_new(user_id, photo):
    photo_id = pic_new(CID_PO_PHOTO, user_id)
    pic_save(photo_id, photo)
    po_photo_save(photo_id, photo)
    #mc_flush(user_id, po_id)
    return photo_id

def po_photo_save(photo_id, photo):
    p1 = pic_fit_width_cut_height_if_large(photo, 721)
    fs_set_jpg('721', photo_id, p1)

def photo_pre_page_and_next_page(po_id):
    id_list = photo_id_list_by_tag_po_id(po_id)
    index = id_list.index(po_id)
    if index == 0:
        return id_list[-1], id_list[index+1]
    elif index == len(id_list) - 1:
        return id_list[index-1], 'tag_list'
    else:
        return id_list[index-1], id_list[index+1]

def photo_id_list_by_tag_po_id(po_id):
    zsite_tag_po = ZsiteTagPo.get(po_id=po_id)
    po_id_list = po_id_list_by_zsite_tag_id(zsite_tag_po.zsite_tag_id)
    return po_id_list

def mc_flush(user_id, po_id):
    po_pic_sum.delete(user_id, po_id)
    mc_pic_id_list.delete('%s_%s' % (user_id, po_id))

if __name__ == '__main__':
    pass
