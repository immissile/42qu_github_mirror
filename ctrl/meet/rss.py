#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.meet import urlmap
from _handler import Base, LoginBase
from model.event import event_all_list

@urlmap('/rss')
class Rss(Base):
    def get(self):
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        limit = 25
        offset = 0
        event_list = event_all_list(limit, offset)
        self.render(
            event_list=event_list,
        )
