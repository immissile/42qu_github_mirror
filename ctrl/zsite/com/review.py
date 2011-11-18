#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase

@urlmap('/review/admin')
class ReviewAdmin(AdminBase):
    def get(self):
        return self.render()


@urlmap('/review')
class Review(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        
        wall = wall_by_from_id_to_id(current_user_id, zsite_id)
        if wall:
            reply_last =  wall.reply_last()
            if reply_last:
                self.render(reply = reply_last)

        self.render()


    def post(self):
        zsite = self.zsite
        current_user = self.current_user
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        txt = self.get_argument('txt', None)

        if txt:
            wall = wall_by_from_id_to_id(current_user_id, zsite_id)
            if wall: 
                reply_last =  wall.reply_last()
            else:
                reply_last = None

            if reply_last:
                reply_last.txt_set(txt)
            else:
                zsite = self.zsite
                from model.reply import STATE_ACTIVE
                zsite.reply_new(current_user,txt,STATE_ACTIVE)
        self.get()
