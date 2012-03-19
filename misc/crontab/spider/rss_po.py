#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.htm2txt import htm2txt
from model.po import po_note_new
from model.po_pic import po_pic_new
from model.state import STATE_RM, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.rss import  RSS_RT_PO
from model.po_show import po_show_new
from model.zsite import Zsite
from model.cid import CID_SITE
import re
from model.zsite_tag import zsite_tag_new_by_tag_id
from model.po_prev_next import mc_flush
from zkit.idf import idf_zhihu
import urllib2
from zkit.urlfetch import urlfetch
from zkit.pic import picopen

exist = {}

def fetch_pic(url, referer=None):
    if url in exist:
        return exist[url]
    headers = {}

    if referer:
        headers['Referer'] = referer

    request = urllib2.Request(url, None, headers)
    raw = urlfetch(request)

    img = picopen(raw)
    exist[url] = img
    return img


class RssPo(object):
    idfer = idf_zhihu()
    def __init__(self, txt, user_id, title, pic_list, state , site_id, tags):
        self.txt, self.user_id, self.title, self.pic_list, self.state, self.site_id,self.tags = txt, user_id, title, pic_list, state, site_id, tags

    def find_dup(self):
        self.idf_list = RssPo.idfer.tf_idf(self.title)
        self.idf_list.sort(key=lambda x:x[1],reverse=True)
        
    def htm2po_by_po(self):
        if self.find_dup():
            return
        txt = self.txt.rstrip()
        if not txt:
            return

        zsite = Zsite.mc_get(self.user_id)

        if zsite.cid == CID_SITE:
            group_id = zsite.id
        else:
            group_id = self.site_id

        po = po_note_new(
            self.user_id, self.title, '', STATE_RM, group_id
        )

        if not po:
            return
        po_id = po.id

        pic_list = self.pic_list

        for seq, url in enumerate(pic_list, 1):
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

