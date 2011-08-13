# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap

@urlmap('/-(\d+)')
class Index(Base):
    def get(Base):
        return self.render()
