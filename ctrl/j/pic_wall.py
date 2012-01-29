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
        po_id, url = next_wall_pic(user_id)
        #self.write('<img src=%s />'%url)
        self.finish(dumps(url))

