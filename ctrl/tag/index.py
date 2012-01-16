# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from ctrl._urlmap.tag import urlmap
from zkit.page import page_limit_offset
from model.po_by_tag import po_by_tag

@urlmap('/')
class Index(Base):
    def get(self):
        page, limit, offset = page_limit_offset(
            "/%s", 100, 1
        )
        current_user_id = self.current_user_id
        items = po_by_tag(1, current_user_id)
        self.render(
            page  = str(page),
            items = items
        )


