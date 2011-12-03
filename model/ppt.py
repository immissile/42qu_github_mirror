#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from model.fs import fs_set, fs_path, fs_url, fs_file
from zkit.sildeshare import slideshare_upload, slideshare_url
from config import SLIDESHARE_KEY, SLIDESHARE_SECRET , SLIDESHARE_USERNAME , SLIDESHARE_PASSWORD
from model.com import com
from model.zsite_com import ZsiteCom
from model.po_video import VIDEO_CID_SLIDESHARE

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
        self.save()

    def publish(self):
        state , swf = slideshare_url(
            SLIDESHARE_KEY, 
            SLIDESHARE_SECRET,
            p.slideshare_id
        )
        if state >= 2:
            self.state = state
            self.save()
            if state == 2:
                com_id = self.com_id
                video_id = video_new(com_id,swf)
                zc = ZsiteCom.mc_get(com_id)
                zc.video_cid = VIDEO_CID_SLIDESHARE
                zc.video_id = video_id
                zc.save()
 
        return sid 

def ppt_new(com_id, ppt):
    p = Ppt(com_id=com_id)
    p.save()
    fs_set('ppt', p.id, 'ppt', ppt)
    return p.id

def ppt_file(id):
    return fs_file('ppt', id, 'ppt')


if __name__ == '__main__':
    id = ppt_new(1, '12345')
    print ppt_file(id)



