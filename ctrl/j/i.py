#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase

@urlmap('/j/career/rm/(\d+)')
class CareerRm(JLoginBase):
    def post(self, id):
        from model.career import career_rm
        current_user_id = self.current_user_id
        career_rm(id, current_user_id)
        self.finish('{}')
