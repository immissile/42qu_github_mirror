#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap

@urlmap('/google_plus')
class Index(Base):
    def get(self):
        q = self.get_argument('q', None)
        if q:
            print q
        return self.render(q=q)

