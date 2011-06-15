#!/usr/bin/env python
#coding:utf-8
import _handler
from model.zsite import Zsite
from _urlmap import urlmap
from model.zsite_list_0 import zsite_show_new, zsite_show_rm

@urlmap('/zsite/(\d+)')
class Index(_handler.Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)

@urlmap('/zsite/show/(\d+)')
class Show(_handler.Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        if zsite:
            zsite_show_new(id)
        self.redirect('/zsite/%s'%id)

@urlmap('/zsite/show/rm/(\d+)')
class ShowRm(_handler.Base):
    def get(self, id):
        zsite_show_rm(id)
        self.redirect('/zsite/%s'%id)
