# -*- coding: utf-8 -*-
from _handler import Base, XsrfGetBase
from ctrl._urlmap_istarsea.istarsea import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        return self.redirect("/auth/reg") 



