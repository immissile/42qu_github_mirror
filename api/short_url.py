#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from _urlmap import urlmap
from model.short_url import url_short, url_short_by_id, url_short_txt
from zweb.json import jsonp
from yajl import dumps

@urlmap('/url/short/(.+)')
class UrlShort(_handler.Base):
    def get(self, id):
        self.finish(url_short_by_id(id))

@urlmap('/url/json/short/(.+)')
class UrlShortJson(_handler.Base):
    def get(self,id):
        self.finish(jsonp(self, dumps(url_short_by_id(id))))
        
