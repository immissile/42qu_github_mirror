# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.search import search_user
from ctrl._util.search import _search


@urlmap('/q')
@urlmap('/q-(\d+)')
class Search(Base):
    search = search_user
    get = search_get
