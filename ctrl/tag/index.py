# -*- coding: utf-8 -*-

from _handler import Base, LoginBase
from ctrl._urlmap.tag import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        self.finish("1345")
