#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env

from model.ppt import Ppt
from model.zsite_com import ZsiteCom
from model.po_video import VIDEO_CID_SLIDESHARE, video_new, video_filter

def update():
    for p in Ppt.where():
        url = ppt_upload(p.com_id)
        zc = ZsiteCom.mc_get(p.com_id)
        video,video_cid = video_filter(url)
        video_id = video_new(p.com_id,video)
        zc.video_cid = video_cid 
        zc.video_id = video_id
        zc.save()
        p.delete()

if __name__ == "__main__":
    update()
