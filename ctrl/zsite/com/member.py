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
from zkit.txt import EMAIL_VALID
from model.user_mail import user_id_by_mail
from model.user_auth import user_new_by_mail
from ctrl.main.auth.__init__ import SHOW_LIST
from zkit.errtip import Errtip

#@urlmap('/member/new/result')
#class MemberNewResult(AdminBase):
#    def get(self):
#        return self.render()

@urlmap('/member/new/search')
class MemberNewSearch(AdminBase):
    search = staticmethod(search_user)
    link = '/member/new/search-%%s?q=%s'
    PAGE_LIMIT = 1024
    get = search_get

    def post(self):
        zsite_id = self.zsite_id

        follow_id_list = self.get_argument('follow_id_list', None)
        if follow_id_list:
            zsite_member_invite(
                self.zsite,
                follow_id_list.split(),
                self.current_user
            )

        return self.redirect(self.request.path)

@urlmap('/member/admin')
class MemberAdmin(AdminBase):
    def get(self):
        self.render()

@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()

    def post(self):
        arguments = self.request.arguments
        for mail, name in zip(arguments['mail'], arguments['name']):
            mail = mail.strip().lower()
            name = name.strip()
            if EMAIL_VALID.match(mail):
                user_id = user_id_by_mail(mail)
                if not user_id:
                    user = user_new_by_mail(mail, name=name)
                    user_id = user.id

                zsite_member_invite(self.zsite, user_id, self.current_user)

        return self.redirect('/review/invite')

@urlmap('/review/invite')
class ReviewInvite(AdminBase):
    def get(self):
        return self.render()

@urlmap('/member/new/reg')
class MemberNewReg(AdminBase):
    def get(self):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        self.render(
            sex=0,
            password='',
            errtip=Errtip(),
            zsite_list=zsite_list,
        )

