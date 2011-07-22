#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.log_history import all_incr, today_all_num

@urlmap('/')
class Index(Base):
    def get(self):
        self.redirect("/chart",permanent=True)

@urlmap('/chart')
class Chart(Base):
    def get(self):
        incr_user, incr_po, incr_pouser, incr_reply = all_incr()
        num_user, num_po, num_pouser, num_reply = today_all_num()
        self.render(
            incr_user=incr_user, incr_po=incr_po, incr_pouser=incr_pouser, incr_reply=incr_reply,
            num_user=num_user, num_po=num_po, num_pouser=num_pouser, num_reply=num_reply
        )
