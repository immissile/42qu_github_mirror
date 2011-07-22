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
        user, po, pouser, reply = all_incr()
        self.render(nuser=user,npo=po,npouser=pouser,nreply=reply)
