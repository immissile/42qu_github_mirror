#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new
from model.po import Po, CID_NOTE
from json import dumps
from zkit.pic import picopen
from model.po_pic import pic_can_add, po_pic_new, po_pic_rm
from model.fs import fs_url_jpg

@urlmap("/j/txt")
class Txt(_handler.Base):
    def get(self):
        self.render()

@urlmap("/j/login")
class Login(_handler.Base):
    def get(self):
        self.render()


#@route
#def btnuph(note_id):
#    man_id = request.man_id
#    if man_id and request.is_post:
#        note_fav_new(note_id, man_id)
#    return 'Y'
#
#
#@route
#def btnup(note_id):
#    man_id = request.man_id
#    if man_id and request.is_post:
#        note_fav_rm(note_id, man_id)
#    return 'Y'
#
#
#@route
#def btndownh(note_id):
#    man_id = request.man_id
#    if man_id and request.is_post:
#        note_hate_new(note_id, man_id)
#    return 'Y'
#
#
#@route
#def btndown(note_id):
#    man_id = request.man_id
#    if man_id and request.is_post:
#        note_hate_rm(note_id, man_id)
#    return 'Y'


#@urlmap("/j/feed/incr/(\d+)")
#class feed_incr(id):
#    def post(self):
#        current_user_id = self.current_user_id
#        if current_user_id:
#            pass
#        self.finish({})
#
#@urlmap("/j/feed/incr_x/(\d+)")
#class feed_incr_x(id):
#    def post(self):
#        self.finish({})
#
#@urlmap("/j/feed/decr/(\d+)")
#class feed_decr(id):
#    def post(self):
#        self.finish({})
#
#@urlmap("/j/feed/decr_x/(\d+)")
#class feed_decr_x(id):
#    def post(self):
#        self.finish({})

@urlmap("/j/note/upload/rm")
@urlmap("/j/note/upload/rm/(\d+)")
class NoteUploadRm(_handler.Base):
    def post(self, id=0):
        seq = self.get_argument('seq')
        user_id = self.current_user_id
        po_pic_rm(user_id, id, seq)
        self.finish('{}')

@urlmap("/j/note/upload")
@urlmap("/j/note/upload/(\d+)")
class NoteUpload(_handler.Base):
    def post(self, id=0):
        #USER DUMPS FIX HEADER FOR FIREFOX
        if id:
            id = int(id)
        r = self._post(id)
        if isinstance(r, (int, long)):
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
            "src": fs_url_jpg(219, pic.id),
            "seqid": pic.seq,
        }

        return r
