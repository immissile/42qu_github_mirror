#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from zkit.pic import pic_fit, pic_square, picopen

@urlmap("/setting")
class Setting(_handler.Base):
    def get(self):
        self.render()

    def post(self):
        files = self.request.files
        self.render()
        if 'pic' in files:
            pic = files['pic']['body']
            img = picopen(img.file)
            if img:
                pos = ""
                if pic_show_id:
                    pic_show_replace(img, pic_show_id)
                else:
                    pic_show_id = pic_show_add(man_id, img)
                pic_show_admin_new(man_id)
                return pic_show_id
            else:
                error.img = "图片格式有误"
                return False
        self.render()
