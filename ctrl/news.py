#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap

@urlmap("/news")
class News(_handler.LoginBase):
    def get(self):
        return self.render()
