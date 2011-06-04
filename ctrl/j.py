#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new
from model.po import Po, CID_NOTE
from json import dumps
from zkit.pic import picopen
from model.po_pic import pic_can_add, po_pic_new
from model.fs import fs_url_jpg

@urlmap("/j/txt")
class Txt(_handler.Base):
    def get(self):
        self.render()

@urlmap("/j/login")
class Login(_handler.Base):
    def get(self):
        self.render()

@urlmap("/j/note/upload")
@urlmap("/j/note/upload/(\d+)")
class NoteUpload(_handler.Base):
    def post(self, id=None):
        #USER DUMPS FIX HEADER FOR FIREFOX
        if id:
            try:
                id = int(id)
            except ValueError:
                id = 0
        r = self._post(id)
        if isinstance(r,(int,long)):
            r = {'status':r}
        r = dumps(r)
        self.finish(r)

    def _post(self, id):
        user_id = self.current_user_id
        if not user_id:
            return 1
        
        files = self.request.files
        img = files.get('img')
        if img:
            img = img[0]['body']
        else:
            return 0
        
        if len(img) > 1024*1024*12:
            return 2

        img = picopen(img)
        if not img:
            return 10

        if id:
            po = Po.mc_get(id)
            if not (
                po 
                and po.user_id == user_id
                and po.cid == CID_NOTE
            ):
                return 0

        if not pic_can_add(user_id, id):
            return 16

        pic = po_pic_new(user_id, id, img)
        if not pic:
            return 14        
 
        r = {
            "status": 0,
            "src": fs_url_jpg(pic.id, 219),
            "seqid": pic.seq,
        }

        return r
