#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.mail_template import STATE_NEW, get_tem_total_by_state, get_tem_by_state
from zkit.page import page_limit_offset

PAGE_LIMIT = 50

@urlmap('/mail/notify')
@urlmap('/mail/notify/(\d+)')
@urlmap('/mail/notify/(\d+)-(\-?\d+)')
class Index(Base):
    def get(self,state=STATE_NEW, n=1):
        total = get_tem_total_by_state(state)
        page, limit, offset = page_limit_offset(
                '/mail/notify/%s-%%s'%state,
                total,
                n,
                PAGE_LIMIT
                )

        mail_template_list = get_tem_by_state(state,limit,offset) 
        self.render(
                mail_template_list = mail_template_list,
                total=total,
                page=page
                )
