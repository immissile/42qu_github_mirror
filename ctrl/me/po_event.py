# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_event import po_event_new

@urlmap('/po/event')
@urlmap('/po/event/(\d+)')
class PoVideo(LoginBase):
    def post(self, po_id=0):
        return self.render()

    def get(self):
        return self.render()



