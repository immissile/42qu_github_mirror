#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.auto_tag import TagSet,tag_po
from yajl import dumps

@urlmap('/po/tag')
class TagGet(Base):
    def post(self):
        name = self.get_argument('name',None)
        if name:
            dumps(self.finish(tag_po.tag_by_name(name)))


