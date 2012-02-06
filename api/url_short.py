#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from _urlmap import urlmap
from model.url_short import url_short, url_short_by_key, url_short_txt
from zweb.json import jsonp
from yajl import dumps

@urlmap('/url/short/([a-zA-Z0-9\-_]+)')
class UrlShort(_handler.Base):
    def get(self, key):
        self.finish(url_short_by_key(key))

@urlmap('/url/short')
class UrlShortJson(_handler.Base):
    def get(self):
        #url = self.get_argument('url', '')
        #link = url_short(url)
        #self.finish(jsonp(self, '"%s"'%link))
        pass

