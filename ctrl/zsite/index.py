#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  _handler
from ctrl._urlmap.zsite import urlmap

@urlmap('/')
class Index(_handler.Base):
    def get(self):
        self.render()
