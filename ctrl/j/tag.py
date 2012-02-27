#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.cid import CID_TAG

@urlmap('/j/tag')
class TagMore(JLoginBase):
    def get(self, n):
        pass  


