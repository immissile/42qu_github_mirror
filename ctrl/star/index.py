# -*- coding: utf-8 -*-
from _handler import Base
from ctrl._urlmap.star import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        self.render()

