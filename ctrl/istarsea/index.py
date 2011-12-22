# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.istarsea import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        return self.redirect("/auth/reg") 



