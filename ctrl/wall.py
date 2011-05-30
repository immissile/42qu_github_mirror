#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.reply import STATE_SECRET, STATE_ACTIVE
from zkit.page import page_limit_offset
from model.wall import Wall

@urlmap("/wall")
class Wall(_handler.LoginBase):
    def get(self):
        zsite = self.zsite
        self.redirect(zsite.link)

    def post(self):
        zsite = self.zsite
        txt = self.get_argument('txt', None)
        if txt:
            secret = self.get_argument('secret', None)
            current_user = self.current_user
            reply = zsite.reply_new(
                current_user.id,
                txt,
                STATE_SECRET if secret else STATE_ACTIVE
            )
        link = zsite.link
        self.redirect(link)

PAGE_LIMIT = 42

@urlmap("/wall/(\-?\d+)")
class Page(_handler.LoginBase):
    def get(self, page):
        zsite = self.zsite
        zsite_link = zsite.link
        page, limit, offset = page_limit_offset(
            "%s/wall/%%s"%zsite_link,
            zsite.reply_total,
            page,
            PAGE_LIMIT
        )
        reply_list = zsite.reply_list_reversed(limit, offset)

        self.render(
            reply_list=reply_list,
            page=page
        )

@urlmap("/wall/txt/(\d+)")
@urlmap("/wall/txt/(\d+)/(\d+)")
class Txt(_handler.LoginBase):
    def get(self, id, page=1):
        zsite = self.zsite
        zsite_link = zsite.link
        page, limit, offset = page_limit_offset(
            "%s/wall/%%s"%zsite_link,
            zsite.reply_total,
            page,
            PAGE_LIMIT
        )
        wall = Wall.mc_get(id)
        self.render(
            wall = wall
        )



