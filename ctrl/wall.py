#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.reply import REPLY_STATE_SECRET, REPLY_STATE_ACTIVE
from zkit.page import page_limit_offset

@urlmap("/wall")
class Wall(_handler.LoginBase):
    def get(self):
        zsite = self.zsite
        return self.redirect(zsite.link)

    def post(self):
        zsite = self.zsite
        txt = self.get_argument('txt', None)
        if txt:
            secret = self.get_argument('secret', None)
            current_user = self.current_user
            reply = zsite.reply_new(
                current_user.id,
                txt,
                REPLY_STATE_SECRET if secret else REPLY_STATE_ACTIVE
            )
        link = zsite.link
        return self.redirect("http://zuroc.com")
        return self.redirect(link)

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
        reply_list = zsite.reply_list(limit, offset)

        return self.render(
            reply_list = reply_list,
            page = page
        )
