#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from model.buzz import buzz_set_read,Buzz

@urlmap('/buzz/rm/(\d+)')
class RmBuzz(ZsiteBase):
    def get(self,id):
        current_user_id = self.current_user_id
        id = int(id)
        buzz = Buzz.get(id)
        if buzz:
            if current_user_id == buzz.to_id:
                buzz_set_read(current_user_id,buzz.id)
        self.redirect("/live")
