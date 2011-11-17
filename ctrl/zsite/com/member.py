#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from ctrl._util.search import search_get
from model.search import search_user
from model.zsite import Zsite
from model.zsite_member import zsite_member_invite
from model.cid import CID_USER

#@urlmap('/member/new/result')
#class MemberNewResult(AdminBase):
#    def get(self):
#        return self.render()

@urlmap('/member/new/search')
class MemberNewSearch(AdminBase):
    search = staticmethod(search_user)
    link = "/member/new/search-%%s?q=%s"
    PAGE_LIMIT = 1024
    get = search_get

    def post(self):
        zsite_id = self.zsite_id

        follow_id_list = self.get_argument('follow_id_list', None)
        if follow_id_list:
            follow_id_list = map(int,follow_id_list.split())

            follow_id_list = [
                i for i in
                Zsite.mc_get_list(follow_id_list)
                if i and i.cid == CID_USER
            ]

            zsite_member_invite(zsite_id, follow_id_list)

        return self.redirect(self.request.path)

@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()

