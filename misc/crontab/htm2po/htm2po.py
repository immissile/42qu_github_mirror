#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from zkit.htm2txt import htm2txt
from model.po import po_note_new, Po
from model.po_pic import po_pic_new
from model.state import STATE_RM, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.rss import rss_po_id_new, RSS_RT_PO, RssPoId
from model.po_show import po_show_new
from model.zsite import Zsite
from model.cid import CID_SITE, CID_USER
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.po_prev_next import mc_flush
from model.txt_img_fetch import txt_img_fetch
import re

    
def htm2po_by_po(pre):
    txt = pre.txt.rstrip()

    if not txt:
        return

    zsite = Zsite.mc_get(pre.user_id)

    if zsite.cid == CID_SITE:
        group_id = zsite.id
    else:
        group_id = pre.site_id

    rp = RssPoId.get(rss_po_id=pre.id)
    if rp:
        po = Po.mc_get(rp.po_id)
        if po:
            po.name_ = pre.title
            po.save()
    else:
        po = po_note_new(
            pre.user_id, pre.title, '', STATE_RM, group_id
        )
        if po and zsite.cid == CID_USER:
            po.rid = pre.rss_id 
            po.save()

    if not po:
        return

    po_id = po.id

    if not rp:
        rss_po_id_new(zsite, pre.id, po_id)

    txt = txt_img_fetch(txt)

    po.txt_set(txt)

    if group_id:
        state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
    else:
        state = STATE_ACTIVE
    po.state = state
    po.save()

    if po.zsite_id != po.user_id:
        zsite_tag_new_by_tag_id(po)

    if pre.state == RSS_RT_PO:
        po_show_new(po)

    mc_flush(po, po.zsite_id)

    return po


