#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.google_plus import google_uid_by_link


@urlmap('/google_plus')
class Index(Base):
    def get(self):
        q = self.get_argument('q', None)
        if q:
            q = google_uid_by_link(q)
        return self.render(q=q)



