#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase

@urlmap('/j/top_notice/rm/(\d+)')
class TopNoticeRm(JLoginBase):
    def post(self, id):
        from model.top_notice import top_notice_rm
        current_user_id = self.current_user_id
        top_notice_rm(id, current_user_id)
        self.finish('{}')
