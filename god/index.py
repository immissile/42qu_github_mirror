#!/usr/bin/env python
#coding:utf-8


import _handler
from zweb._urlmap import urlmap
from model.zsite import Zsite

@urlmap("/")
class Index(_handler.Base):
    def get(self):
        self.render()

@urlmap("/chart")
class Chart(_handler.Base):
    def get(self):
        self.render()

@urlmap("/zsite/(\d+)")
class Zsite(_handler.Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)

