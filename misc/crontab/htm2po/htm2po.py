#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetch_pic import fetch_pic

import json
from zkit.htm2txt import htm2txt
from model.po import po_note_new, Po
from model.po_pic import po_pic_new
from model.state import STATE_RM, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.rss import rss_po_id, RSS_RT_PO, RssPoId
from model.po_show import po_show_new
from model.zsite import Zsite
from model.cid import CID_SITE
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.po_prev_next import mc_flush
import zkit.idf import idf_zhihu

class RssPo(object):
    idfer = idf_zhihu()
    def __init__(self, txt, user_id, title, pic_list, state , site_id):
        self.txt, self.user_id, self.title, self.pic_list, self.state, self.site_id = txt, user_id, title, pic_list, state, site_id

    def find_dup(self):
        self.idf_list = RssPo.idfer.tf_idf(self.txt+self.title)
        
    def htm2po_by_po(self):
        txt = self.txt.rstrip()
        if not txt:
            return

        zsite = Zsite.mc_get(self.user_id)

        if zsite.cid == CID_SITE:
            group_id = zsite.id
        else:
            group_id = self.site_id

        rp = RssPoId.get(self.id)
        if rp:
            po = Po.mc_get(rp.po_id)
            if po:
                po.name_ = self.title
                po.save()
        else:
            po = po_note_new(
                self.user_id, self.title, '', STATE_RM, group_id
            )

        if not po:
            return
        po_id = po.id

        if not rp:
            rss_po_id(self.id, po_id)


        pic_list = json.loads(self.pic_list)

        for seq, url in enumerate(pic_list, 1):
            if '.feedsky.com/' in url:
                img = None
            else:
                img = fetch_pic(url)
                if img:
                    x, y = img.size
                    if x < 48 and y < 48:
                        img = None

            if img:
                po_pic_new(self.user_id, po_id, img, seq)
            else:
                txt = re.sub('\s*图:%s\s*'%seq, '', txt, re.MULTILINE)

        po.txt_set(txt)

        if group_id:
            state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
        else:
            state = STATE_ACTIVE
        po.state = state
        po.save()

        if po.zsite_id != po.user_id:
            zsite_tag_new_by_tag_id(po)

        po.feed_new()
        if self.state == RSS_RT_PO:
            po_show_new(po)

        mc_flush(po, po.zsite_id)

        return po



def htm2po_by_po(pre):
    txt = pre.txt.rstrip()
    if not txt:
        return

    zsite = Zsite.mc_get(pre.user_id)

    if zsite.cid == CID_SITE:
        group_id = zsite.id
    else:
        group_id = pre.site_id

    rp = RssPoId.get(pre.id)
    if rp:
        po = Po.mc_get(rp.po_id)
        if po:
            po.name_ = pre.title
            po.save()
    else:
        po = po_note_new(
            pre.user_id, pre.title, '', STATE_RM, group_id
        )

    if not po:
        return
    po_id = po.id

    if not rp:
        rss_po_id(pre.id, po_id)


    pic_list = json.loads(pre.pic_list)

    for seq, url in enumerate(pic_list, 1):
        if '.feedsky.com/' in url:
            img = None
        else:
            img = fetch_pic(url)
            if img:
                x, y = img.size
                if x < 48 and y < 48:
                    img = None

        if img:
            po_pic_new(pre.user_id, po_id, img, seq)
        else:
            txt = re.sub('\s*图:%s\s*'%seq, '', txt, re.MULTILINE)

    po.txt_set(txt)

    if group_id:
        state = STATE_PO_ZSITE_SHOW_THEN_REVIEW
    else:
        state = STATE_ACTIVE
    po.state = state
    po.save()

    if po.zsite_id != po.user_id:
        zsite_tag_new_by_tag_id(po)

    po.feed_new()
    if pre.state == RSS_RT_PO:
        po_show_new(po)

    mc_flush(po, po.zsite_id)

    return po


