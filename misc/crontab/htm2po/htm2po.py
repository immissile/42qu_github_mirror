#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetch_pic import fetch_pic

import json
from zkit.htm2txt import htm2txt
from model.po import po_note_new
from model.po_pic import po_pic_new
from model.state import STATE_DEL, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.rss import rss_po_id, RSS_RT_PO
from model.po_show import po_show_new
from model.zsite import Zsite
from model.cid import CID_SITE

def htm2po_by_po(pre):
    txt = pre.txt.rstrip()
    if not txt:
        return
       
    zsite = Zsite.mc_get(pre.user_id)
    
    if zsite.cid == CID_SITE: 
        group_id = zsite.id
    else:
        group_id = 0

    po = po_note_new(
        pre.user_id, pre.title, '', STATE_DEL, group_id
    )

    if not po:
        return    

    po_id = po.id

    rss_po_id(pre.id, po_id)

    pic_list = json.loads(pre.pic_list)

    for seq, url in enumerate(pic_list, 1):
        img = fetch_pic(url)
        if img:
            po_pic_new(pre.user_id, po_id, img, seq)
        else:
            txt = txt.replace("图:%s"%seq,"")

    po.txt_set(txt)

    if group_id:
        state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
    else:
        state = STATE_ACTIVE
    po.state = state
    po.save()

    po.feed_new()
    if pre.state == RSS_RT_PO:
        po_show_new(po)


    return po


