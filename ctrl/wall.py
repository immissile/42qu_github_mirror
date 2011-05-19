#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.reply import REPLY_STATE_SECRET, REPLY_STATE_ACTIVE

@urlmap("/wall")
class Wall(_handler.LoginBase):
    def get(self):
        zsite = self.zsite
        return self.redirect(zsite.link)

    def post(self):
        zsite = self.zsite
        txt = self.get_argument('txt',None)
        if txt:
            secret = self.get_argument('secret', None)
            current_user = self.current_user
            reply = zsite.reply_new(
                current_user.id,
                txt,
                REPLY_STATE_SECRET if secret else REPLY_STATE_ACTIVE
            )


        return self.redirect(zsite.link)


@urlmap("/wall/(\-?\d+)")
class Page(_handler.LoginBase):
    def get(self, page):
        return self.render()

