#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from cgi import escape
from zkit.pic import pic_fit_width_cut_height_if_large
from pic import pic_new, pic_save, PicMixin
from cid import CID_PHOTO
from fs import fs_set_jpg, fs_url_jpg
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from po_pic import PoPic
from zsite_tag import ZsiteTagPo, zsite_tag_new_by_tag_id

mc_po_photo_prev_next = McCacheM("PoPhotoPrev*%s")


PIC_SIZE = 721

def photo_new(user_id, photo):
    photo_id = pic_new(CID_PHOTO, user_id)
    pic_save(photo_id, photo)
    po_photo_save(photo_id, photo)
    return photo_id

def po_photo_save(photo_id, photo):
    p1 = pic_fit_width_cut_height_if_large(photo, 721)
    fs_set_jpg('721', photo_id, p1)
    p1 = pic_fit_width_cut_height_if_large(photo, 677)
    fs_set_jpg('677', photo_id, p1)

@mc_po_photo_prev_next("{zsite_id}_{po_id}_{tag_id}")
def po_photo_prev_next(zsite_id, po_id, tag_id):
    t = ZsiteTagPo.get(zsite_id=zsite_id, po_id=po_id, zsite_tag_id=tag_id)
    if not t:
        result = (None, None)
    else:
        id = t.id 
        result = (
            _po_photo_goto(
                'select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and cid=%s and id>%s order by id limit 1',
                zsite_id,
                tag_id,
                id,
            )
            ,
            _po_photo_goto(
                'select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and cid=%s and id<%s order by id desc limit 1',
                zsite_id,
                tag_id,
                id,
            )
        )
   
    if result[0] != result[1]:
        if result[0] is None:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and cid=%s order by id desc limit 1',
                zsite_id,
                tag_id,
                CID_PHOTO, 
            )
            result[0] = c.fetchone()[0] 
        elif result[1] is None:
            c = ZsiteTagPo.raw_sql(
                'select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and cid=%s order by id limit 1',
                zsite_id,
                tag_id
                CID_PHOTO, 
            )
            result[1] = c.fetchone()[0]
    return result


def _po_photo_goto(sql, zsite_id, zsite_tag_id, id):
    c = ZsiteTagPo.raw_sql(
        sql,
        zsite_id,
        zsite_tag_id, 
        CID_PHOTO, 
        id
    )
    r = c.fetchone()
    if r:
        r = r[0]
    return r

def mc_flush(zsite_id, zsite_tag_id, id, po_id):
    _mc_flush(
        "select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and id>%s and cid=%s order by id limit 1",
        zsite_id,
        zsite_tag_id,
        id
    )
    _mc_flush( 
        "select po_id from zsite_tag_po where zsite_id=%s and zsite_tag_id=%s and id<%s and cid=%s order by id desc limit 1",
        zsite_id,
        zsite_tag_id,
        id
    )
    mc_po_photo_prev_next.delete("%s_%s_%s"%(zsite_id, zsite_tag_id, po_id))


def _mc_flush(sql, zsite_id, zsite_tag_id, id):
    c = ZsiteTagPo.raw_sql(
        sql,
        zsite_id,
        zsite_tag_id,
        id,
        CID_PHOTO,
    )
    r = c.fetchone()
    if r:
        mc_po_photo_prev_next.delete("%s_%s_%s"%(zsite_id, r[0], zsite_tag_id))



def po_photo_new(user_id, name, txt, img, state=STATE_ACTIVE):

    if not name and not txt:
        return

    name = name or time_title()
    if not is_same_post(user_id, name, txt):

        rid = photo_new(user_id, img)

        m = po_new(CID_PHOTO, user_id, name, state, rid)
        id = m.id
        m.txt_set(txt)
        if state > STATE_SECRET:
            m.feed_new()

        zsite_tag_new_by_tag_id(m, 1)

        return m


if __name__ == '__main__':
    pass
