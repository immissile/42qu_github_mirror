#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import JLoginBase, Base
from yajl import dumps
from ctrl._urlmap.j import urlmap
from model.po_pic_show import next_wall_pic

@urlmap('/j/pic_wall')
class PicWall(JLoginBase):
    def get(self):
        user_id = self.current_user_id
        thumb , url, po = next_wall_pic(user_id)
        result = [
                thumb,
                url,
                po.name,
                po.txt
                ]
        self.finish(dumps(result))

       # self.write('<img src=%s />'%thumb)
       # self.write('<img src=%s />'%url)

       # self.write('<a href="/%s">LINK</a>'%po.id)
