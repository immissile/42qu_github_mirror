#!/usr/bin/env python
#coding:utf-8
from model.zsite import Zsite
from zweb._urlmap import urlmap


@urlmap("/zsite/(\d+)")
class Index(_handler.Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)


