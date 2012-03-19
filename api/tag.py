#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from _urlmap import urlmap
from model.autocomplete import autocomplete_tag
from yajl import dumps
from zweb.json import jsonp
from cgi import escape

@urlmap('/tag')
class TagGet(Base):

    def get(self):
        q = self.get_argument('q',None)
        if q:
            result = dumps((int(i[0]),int(i[1]),escape(i[2])) for i in autocomplete_tag.id_rank_name_list_by_str(q)) 
        else:
            result = []

        self.finish(jsonp(self,result))
        
    post = get

