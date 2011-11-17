#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from ctrl._util.search import search_get
from model.search import search_user

#@urlmap('/member/new/result')
#class MemberNewResult(AdminBase):
#    def get(self):
#        return self.render()

@urlmap('/member/new/search')
@urlmap('/member/new/search-(\d+)')
class MemberNewSearch(AdminBase):
    search = staticmethod(search_user)
    link = "/member/new/search-%%s?q=%s"
    get = search_get


@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()

