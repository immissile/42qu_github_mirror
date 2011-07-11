# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.main import urlmap
from model.zsite_tag import ZsiteTag
from model.zsite import Zsite
from config import SITE_DOMAIN

@urlmap('/-(\d+)')
class Index(Base):
    def get(self, id):
        return self.redirect("//%s.%s"%(id,SITE_DOMAIN))
    
    post = get


