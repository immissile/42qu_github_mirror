#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap

@urlmap('/import_feed')
class ImportFeed(Base):
    def get(self):
        self.render()
