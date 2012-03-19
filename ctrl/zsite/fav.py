#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, login
from ctrl._urlmap.zsite import urlmap
from model.fav import fav_po_list_by_user_id_cid, fav_po_count_by_user_id_cid
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_VIDEO, CID_AUDIO, CID_EVENT
from zkit.page import page_limit_offset
from model.po import Po
from model.zsite import Zsite

@urlmap('/fav')
class Index(ZsiteBase):
    def get(self):
        self.render()

PAGE_LIMIT = 42

class FavPage(ZsiteBase):
    cid = 0
    template = '/ctrl/zsite/po_view/po_page.htm'

    def get(self, n=1):
        zsite_id = self.zsite_id
        cid = self.cid
        page_template = self.page_template
        total = fav_po_count_by_user_id_cid(zsite_id, cid)
        n = int(n)

        page, limit, offset = page_limit_offset(
            page_template,
            total,
            n,
            PAGE_LIMIT
        )

        if n != 1 and offset >= total:
            return self.redirect(page_template[:-3])

        li = fav_po_list_by_user_id_cid(zsite_id, cid, limit, offset)

        if cid == CID_WORD:
            rid_po_list = [i for i in li if i.rid]
            Po.mc_bind(rid_po_list, 'question', 'rid')
            Zsite.mc_bind([i.target for i in rid_po_list], 'user', 'user_id')

        self.render(
            cid=cid,
            total=total,
            li=li,
            page=page,
            back_a='/fav',
        )

@urlmap('/fav/word')
@urlmap('/fav/word-(\d+)')
class WordPage(FavPage):
    cid = CID_WORD
    page_template = '/fav/word-%s'


@urlmap('/fav/note')
@urlmap('/fav/note-(\d+)')
class NotePage(FavPage):
    cid = CID_NOTE
    page_template = '/fav/note-%s'


@urlmap('/fav/question')
@urlmap('/fav/question-(\d+)')
class QuestionPage(FavPage):
    cid = CID_QUESTION
    page_template = '/fav/question-%s'


@urlmap('/fav/photo')
@urlmap('/fav/photo-(\d+)')
class PhotoPage(FavPage):
    cid = CID_PHOTO
    page_template = '/fav/photo-%s'


@urlmap('/fav/video')
@urlmap('/fav/video-(\d+)')
class VideoPage(FavPage):
    cid = CID_VIDEO
    page_template = '/fav/video-%s'


@urlmap('/fav/audio')
@urlmap('/fav/audio-(\d+)')
class AudioPage(FavPage):
    cid = CID_AUDIO
    page_template = '/fav/audio-%s'


@urlmap('/fav/answer')
@urlmap('/fav/answer-(\d+)')
class AnswerPage(FavPage):
    cid = CID_ANSWER
    page_template = '/fav/answer-%s'


@urlmap('/fav/event')
@urlmap('/fav/event-(\d+)')
class EventPage(FavPage):
    cid = CID_EVENT
    page_template = '/fav/event-%s'
    template = 'ctrl/zsite/event/event_page.htm'

