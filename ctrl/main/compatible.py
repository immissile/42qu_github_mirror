# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.main import urlmap
from model.zsite_tag import ZsiteTag
from model.zsite import Zsite

@urlmap('/-\d+')
class Index(Base):
    pass

