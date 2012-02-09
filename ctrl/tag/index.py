# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from ctrl._urlmap.tag import urlmap
from zkit.page import page_limit_offset
from model.po_by_tag import po_id_list_by_tag_id



@urlmap('/')
@urlmap('/-(\d+)')
class Index(Base):
    def get(self,n=1):
        total = 100
        page, limit, offset = page_limit_offset(
            "/-%s", total, n
        )
        current_user_id = self.current_user_id
        items = po_id_list_by_tag_id(47036, current_user_id, limit, offset )
        self.render(
            page  = str(page),
            total = total,
            items = items
        )
