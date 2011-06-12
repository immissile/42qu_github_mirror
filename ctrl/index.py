#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zsite import  _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new

@urlmap('/')
class Index(_handler.Base):
    def get(self):
        self.render()



