#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from model.fs import fs_set, fs_path, fs_url, fs_file
from zkit.slideshare import slideshare_upload, slideshare_url
from config import SLIDESHARE_KEY, SLIDESHARE_SECRET , SLIDESHARE_USERNAME , SLIDESHARE_PASSWORD
from model.zsite_com import ZsiteCom
from model.po_video import video_new
from model.video_swf import VIDEO_CID_SLIDESHARE
from time import time
from model.gid import gid

def com_ppt_set(com_id, video_id=0):
    zc = ZsiteCom.mc_get(com_id)
    if zc is None:
        zc = ZsiteCom(com_id=com_id)
    if video_id is False:
        zc.video_cid = 0
        zc.video_id = 0
    else:
        zc.video_cid = VIDEO_CID_SLIDESHARE
        zc.video_id = video_id
    zc.save()

STATE_PPT_CONVERTED = 2
STATE_PPT_CONVERTE_FAILED = 3

class Ppt(Model):
    def upload(self):
        id = self.id
        sid = slideshare_upload(
            SLIDESHARE_KEY,
            SLIDESHARE_SECRET,
            SLIDESHARE_USERNAME,
            SLIDESHARE_PASSWORD,
            ppt_file(id)
        )
        self.state = 1
        self.slideshare_id = sid
        self.time = int(time())
        self.save()

    def publish(self):
        state , swf = slideshare_url(
            SLIDESHARE_KEY,
            SLIDESHARE_SECRET,
            self.slideshare_id
        )
        if state >= STATE_PPT_CONVERTED:
            com_id = self.com_id
            self.state = state
            self.save()
            vid = False
            if state == STATE_PPT_CONVERTED:
                vid = gid()
                video_new(vid, swf)
            com_ppt_set(com_id, vid)
        else:
            self.time = int(time())
            self.save()

def ppt_new(com_id, ppt):
    p = Ppt(com_id=com_id)
    p.save()
    fs_set('ppt', p.id, 'ppt', ppt)
    com_ppt_set(com_id)
    return p.id

def ppt_file(id):
    return fs_file('ppt', id, 'ppt')


if __name__ == '__main__':
    id = ppt_new(1, '12345')
    print ppt_file(id)



