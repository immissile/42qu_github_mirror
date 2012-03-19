# -*- coding: utf-8 -*-
from _handler import Base, LoginBase
from ctrl._urlmap.hero import urlmap
from model.search import search_user
from ctrl._util.search import search_get


@urlmap('/q')
@urlmap('/q-(\d+)')
class Search(Base):
    def get(self, n=1):
        if not self.get_argument('q',None):
            return self.redirect("/")
        return search_get(self, n)

    search = staticmethod(search_user)


