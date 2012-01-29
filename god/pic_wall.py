#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.po_pic_show import PicWallPics, STATE_INIT, pic_set_state, STATE_IGNORE, STATE_WAIT
from zkit.page import page_limit_offset

PAGE_LIMIT = 50

@urlmap('/pic_wall')
@urlmap('/pic_wall-(\d+)')
class PicWall(Base):
    def get(self,n=1):
        qs = PicWallPics.where(state=STATE_INIT)
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/event-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        self.render(
            'god/pic_wall/pic_wall.htm',
            li=li,
            page=page,
        )

@urlmap('/allow/(\d+)')
class AllowPic(Base):
    def get(self,n):
        pic_set_state(n,STATE_WAIT)
        self.redirect("/pic_wall")

@urlmap('/disallow/(\d+)')
class DisallowPic(Base):
    def get(self,n):
        pic_set_state(n,STATE_IGNORE)
        self.redirect("/pic_wall")
