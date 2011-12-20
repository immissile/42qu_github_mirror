# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.zsite_show import zsite_show_list, zsite_show_count
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite import Zsite
from config import SITE_DOMAIN

def hero_page(n):
    n = int(n)
    count = zsite_show_count(CID_USER)
    page, limit, offset = page_limit_offset(
        '//hero.%s/-%%s'%SITE_DOMAIN,
        count,
        n,
        64
    )
    zsite_list = zsite_show_list(CID_USER, limit, offset)
    return zsite_list, page

@urlmap('/')
@urlmap('/-(\d+)')
class Index(Base):
    def get(self, n=1):
        zsite_list , page = hero_page(n)
        self.render(zsite_list=zsite_list, page=page)


@urlmap("/q/school")
class School(Base):
    def get(self, n=1):
        zsite_list , page = hero_page(n)
        self.render(zsite_list=zsite_list, page=page)
