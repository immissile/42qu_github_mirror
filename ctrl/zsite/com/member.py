#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from ctrl._util.search import search_get
from model.search import search_user
from model.zsite import Zsite
from zkit.txt import EMAIL_VALID
from model.user_mail import user_id_by_mail
from model.user_auth import user_new_by_mail
from zkit.errtip import Errtip
from model.com_apply import com_apply_new, com_apply_get, com_apply_rm, com_apply_accept
from model.zsite_member import zsite_member_rm, zsite_member_new, ZSITE_MEMBER_STATE_ACTIVE, zsite_id_count_by_member_admin, zsite_member_is_invite
from zkit.txt import EMAIL_VALID
from model.zsite_url import id_by_url
from model.zsite import zsite_by_query
from itertools import chain
from model.zsite_com_invite import zsite_member_invite, zsite_review_invite

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
        self.render(com_id=self.zsite_id)

@urlmap('/member/join')
class MemberJoin(LoginBase):
    def get(self):
        user_id = self.current_user_id
        com_id = self.zsite_id
        if zsite_member_is_invite(com_id, user_id):
            zsite_member_new(com_id, user_id, ZSITE_MEMBER_STATE_ACTIVE)
        else:
            com_apply_new(com_id, user_id)
        self.redirect('/')

def _invite_member(self, mail_name_list):

    for mail, name in mail_name_list:
        mail = mail.strip().lower()
        name = name.strip()
        if EMAIL_VALID.match(mail):
            user_id = user_id_by_mail(mail)
            if not user_id:
                user = user_new_by_mail(mail, name=name)
                user_id = user.id

            zsite_member_invite(self.zsite, user_id, self.current_user)

def _invite(self):
    arguments = self.request.arguments

    _invite_member(self, zip(arguments.get('mail', ()), arguments.get('name', ())))


@urlmap('/member/admin/invite')
class MemberAdminInvite(AdminBase):
    def get(self):
        self.render()

    _invite = _invite

    def post(self):
        com = self.zsite
        current_user = self.current_user

        links = self.get_arguments('link', ())
        uids = filter(bool, map(zsite_by_query, links))
        zsite_member_invite(com, uids, current_user)

        self._invite()
        self.render(success=True)



@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()

    _invite = _invite

    def post(self):
        self._invite()
        return self.redirect('/review/invite')


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


