#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.auto_tag import autocomplete_tag
from yajl import dumps
from zweb.json import jsonp
from cgi import escape

@urlmap('/po/tag')
class TagGet(Base):

    def get(self):
        name = self.get_argument('q',None)
        if name:
            result = dumps((int(i[0]),int(i[1]),escape(i[2])) for i in autocomplete_tag.id_rank_name_list_by_str(name)) 

        self.finish(jsonp(self,result))
    post = get

