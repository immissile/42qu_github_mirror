#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from model.zsite_com import com_pic_new, zsite_com_new
from model.po_video import video_new, video_filter
from zkit.pic import picopen
@urlmap('/bio/new')
class BioNew(AdminBase):
    def get(self):
        print self.request.arguments
        return self.render()

    def post(self):
        hope = self.get_argument('hope',None)
        money = self.get_argument('money',None)
        culture = self.get_argument('culture',None)
        team = self.get_argument('team',None)
        video = self.get_argument('video',None)
        com_id = self.zsite.id
        files = self.request.files
        cover_id = None
        
        if files.get('cover'):
            cover = files['cover'][0]['body']
            if cover:
                cover = picopen(cover)
                print cover,'!!!'
                if cover:
                    cover_id = com_pic_new(com_id,cover)
        
        if files.get('pic'):
            for pic in files['pic']:
                if pic['body']:
                    pic = picopen(pic['body'])
                    if pic:
                        com_pic_new(com_id,pic)
        
        if video:
            video,video_site = video_filter(video)
            video_new(com_id,video)
        zsite_com_new(com_id,hope,money,culture,team,cover_id,video_site)
        self.redirect('/')


