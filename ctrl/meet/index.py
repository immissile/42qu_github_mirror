# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase

@urlmap('/-(\d+)')
class Index(Base):
    def get(Base):
        return self.render()
