#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from _urlmap import urlmap
from model.url_short import url_short, url_short_by_id, url_short_txt
from zweb.json import jsonp
from yajl import dumps

@urlmap('/url/short/(\d+)')
class UrlShort(_handler.Base):
    def get(self, id):
        self.finish(url_short_by_id(id))

@urlmap('/url/short/jsonp/(\d+)')
class UrlShortJson(_handler.Base):
    def get(self,id):
        self.finish(jsonp(self, dumps(url_short_by_id(id))))
        
