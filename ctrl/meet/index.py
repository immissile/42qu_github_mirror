# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        return self.render()
