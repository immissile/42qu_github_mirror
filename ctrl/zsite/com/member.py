#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase


@urlmap('/member/new/search')
class MemberNewSearch(AdminBase):
    def get(self):
        return self.render()


@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()
