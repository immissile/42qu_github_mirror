#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import dumps
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.po import Po, CID_WORD
from zkit.pic import picopen
from model.po_pic import pic_can_add, po_pic_new, po_pic_rm
from model.fs import fs_url_jpg
from model.zsite_tag import zsite_tag_list_by_zsite_id_with_init, tag_id_by_po_id,\
zsite_tag_new_by_tag_id, zsite_tag_new_by_tag_name, zsite_tag_rm_by_tag_id, zsite_tag_rename


@urlmap('/j/po/tag/edit')
class TagEdit(JLoginBase):
    def post(self):
        current_user_id = self.current_user_id
        tag_list = self.get_arguments('tag')
        name_list = self.get_arguments('name')
        for tag_id, tag_name in zip(tag_list, name_list):
            zsite_tag_rename(current_user_id, tag_id, tag_name) 
        self.finish('{}')

@urlmap('/j/po/tag')
class Tag(JLoginBase):
    def get(self):
        current_user_id = self.current_user_id
        tag_list = zsite_tag_list_by_zsite_id_with_init(current_user_id)
        self.finish(dumps(tag_list.iteritems()))

@urlmap('/j/po/tag/rm/(\d+)')
class TagRm(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id
        zsite_tag_rm_by_tag_id(current_user_id, id)
        self.finish("{}")

@urlmap('/j/po/note/upload/rm')
@urlmap('/j/po/note/upload/rm/(\d+)')
class NoteUploadRm(JLoginBase):
    def post(self, id=0):
        seq = self.get_argument('seq')
        user_id = self.current_user_id
        po_pic_rm(user_id, id, seq)
        self.finish('{}')

@urlmap('/j/po/note/upload')
@urlmap('/j/po/note/upload/(\d+)')
class NoteUpload(JLoginBase):
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
                and po.cid != CID_WORD
            ):
                return 0

        if not pic_can_add(user_id, id):
            return 16

        pic = po_pic_new(user_id, id, img)
        if not pic:
            return 14

        r = {
            'status': 0,
            'src': fs_url_jpg(219, pic.id),
            'seqid': pic.seq,
        }

        return r
