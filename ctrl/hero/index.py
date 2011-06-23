# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.zsite_list_0 import zsite_show
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite import Zsite

@urlmap('/')
class Index(Base):
    def get(self):
        zsite_list = Zsite.mc_get_list(zsite_show(16, 0))
        self.render(zsite_list=zsite_list)
