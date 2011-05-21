#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from zkit.pic import picopen
from model.pic import ico_new
from tornado.web import authenticated

@urlmap("/setting")
class Setting(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        files = self.request.files
        current_user = self.current_user
        error_img = None
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                ico_new(current_user.id, pic)
            else:
                error_img = "图片格式有误"
        self.render(
           error_img=error_img
        )
