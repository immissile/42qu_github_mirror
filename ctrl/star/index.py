# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.star import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        self.render()

@urlmap('/new')
class New(Base):
    def get(self):
        self.render()

