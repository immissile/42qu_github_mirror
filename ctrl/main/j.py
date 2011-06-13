#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from model.vote import vote_state
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new
from model.po import Po, CID_NOTE
from json import dumps
from zkit.pic import picopen
from model.po_pic import pic_can_add, po_pic_new, po_pic_rm
from model.fs import fs_url_jpg
from model.vote import vote_decr_x, vote_decr, vote_incr_x, vote_incr
from model.feed_render import MAXINT, PAGE_LIMIT, render_feed_by_zsite_id
from model.feed import feed_rt, feed_rm_rt, feed_rt_id


@urlmap('/j/rt/(\d+)')
class Rt(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rt(current_user_id, id)
        self.finish("{}")


@urlmap('/j/rt/rm/(\d+)')
class RtRm(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        if current_user_id:
            feed_rm_rt(current_user_id, id)
        self.finish("{}")


@urlmap('/j/txt')
class Txt(_handler.Base):
    def get(self):
        self.render()


@urlmap('/j/login')
class Login(_handler.Base):
    def get(self):
        self.render()


@urlmap('/j/feed/incr1/(\d+)')
class FeedIncr(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_incr(current_user_id, id)
        self.finish('{}')


@urlmap('/j/feed/incr0/(\d+)')
class FeedIncrX(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_incr_x(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/decr1/(\d+)')
class FeedDecr(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_decr(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/decr0/(\d+)')
class FeedDecrX(_handler.JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        vote_decr_x(current_user_id, id)
        self.finish('{}')


@urlmap('/j/feed')
class Feed(_handler.JLoginBase):
    def get(self, id=MAXINT):
        current_user_id = self.current_user_id

        result = render_feed_by_zsite_id(current_user_id, PAGE_LIMIT, id)
        for i in result:
            id = i[0]
            i.insert(7, vote_state(current_user_id, id))
            i.insert(7, is_rt(current_user_id, id))
             
        self.finish(dumps(result))

    post = get

@urlmap('/j/note/upload/rm')
@urlmap('/j/note/upload/rm/(\d+)')
class NoteUploadRm(_handler.JLoginBase):
    def post(self, id=0):
        seq = self.get_argument('seq')
        user_id = self.current_user_id
        po_pic_rm(user_id, id, seq)
        self.finish('{}')

@urlmap('/j/note/upload')
@urlmap('/j/note/upload/(\d+)')
class NoteUpload(_handler.JLoginBase):
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
                and po.cid == CID_NOTE
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
