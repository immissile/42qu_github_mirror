#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.auto_tag import TagSet,tag_tag
from yajl import dumps


@urlmap('/po/tag/(.*)')
@urlmap('/po/tag')
class TagGet(Base):
    def handle_tag(self,name):
        if name:
            self.finish(dumps(tag_tag.tag_by_name(name)))

    def post(self):
        name = self.get_argument('name',None)
        self.handle_tag(name)

    def get(self,name):
        self.handle_tag(name)

