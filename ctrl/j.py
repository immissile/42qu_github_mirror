#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from model.follow import follow_rm, follow_new

@urlmap("/j/txt")
class Txt(_handler.Base):
    def get(self):
        self.render()

