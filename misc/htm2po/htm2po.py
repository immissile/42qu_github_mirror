#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetch_pic import fetch_pic


from zkit.htm2txt import htm2txt
from model.po import po_note_new
from model.po_pic import po_pic_new
from model.state import STATE_SECRET

def htm2po(user_id, title, htm):
    po = po_note_new(user_id, title, '', STATE_SECRET)
    po_id = po.id
    try:
        txt, pic_list = htm2txt(htm)
    except:
        po.txt_set(htm)
    else:
        for seq, url in enumerate(pic_list, 1):
            img = fetch_pic(url)
            if img:
                po_pic_new(user_id, po_id, img, seq)
        po.txt_set(txt)
    return po
