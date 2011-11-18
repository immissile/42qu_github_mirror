#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase


@urlmap('/bio/new')
class BioNew(AdminBase):
    def get(self):
        print self.request.arguments
        return self.render()

    def post(self):
        print self.request.arguments
        pics = self.request.files
        print pics.keys()
        self.get()


