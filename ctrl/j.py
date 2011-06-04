#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new

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
    def _post(self, id=None):
        user_id = self.current_user_id
        if not user_id:
            return 1
        return 2
    
    def post(self, id=None):
        r = self._post(id)
        if isinstance(r,(int,long)):
            r = {'status':r}
        self.finish(r)

    get = post

   #     form = request.form
   #     img = form.img

   #     try:
   #         note_id = int(note_id)
   #     except ValueError:
   #         note_id = 0

   #     if not (man_id and request.is_post and 'img' in form and img is not None and img.filename):
   #         return ''

   #     if note_id:
   #         note = Note.mc_get(note_id)
   #         if not (note and note.man_id==man_id and note.txt_len):
   #             return ''

   #     img = img.file.read()
   #     if len(img) > 1024*1024*3:
   #         r = '{"status": 2}'
   #     else: 
   #         img = picopen(img)
   #         if not img:
   #             r =  '{"status":10})'

   #         elif not Note.can_new_pic(man_id, note_id):
   #             '{"status":16}'
   #         else:
   #             pic = Note.new_pic(man_id, note_id, img)
   #             if not pic:
   #                 r = '{"status":14}'
   #             else:
   #                 r = {
   #                     "status": 0,
   #                     "src": Note.pic_url_by_id(pic.id, 219),
   #                     "seqid": pic.order,
   #                 }
   #     self.finish(r)

