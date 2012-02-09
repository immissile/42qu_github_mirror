#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.auto_tag import auto_complete_tag
from yajl import dumps
from zweb.json import jsonp

@urlmap('/po/tag')
class TagGet(Base):

    def post(self):
        name = self.get_argument('q',None)
        result = dumps((int(i[0]),int(i[1]),i[2]) for i in auto_complete_tag.id_name_list_by_name_list(name)) 
        self.finish(jsonp(self,result))

    get = post
