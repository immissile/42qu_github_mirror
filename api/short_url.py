#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from _urlmap import urlmap
from model.short_url import url_short, url_short_by_id, url_short_txt

@urlmap('/url/short/(.+)')
class UrlShort(_handler.Base):
    def get(self, id):
        self.finish(url_short_by_id(id))
