# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.zsite_admin import zsite_list_by_admin_id
from model.state import STATE_APPLY
from zkit.page import page_limit_offset

PAGE_LIMIT = 20

@urlmap('/site')
class List(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        zsite_list = zsite_list_by_admin_id(current_user_id)
        self.render(zsite_list=zsite_list)
