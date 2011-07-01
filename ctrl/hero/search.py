# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.zsite import Zsite
from model.search import search

@urlmap('/q')
class Search(Base):
    def get(self):
        q = self.get_argument('q', '')
        if q:
            try:
                q = q.decode('utf-8')
            except UnicodeDecodeError:
                q = q.decode('gb18030')
            q = q.encode('utf-8')
            id_list, total = search(q, offset, list_limit)
            zsite_list = Zsite.mc_get_list(id_list)
