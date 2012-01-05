#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap

@urlmap('/tag')
class Index(Base):
    def get(self):
        return self.render()



