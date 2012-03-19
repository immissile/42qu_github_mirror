#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from model.zsite_member import zsite_member_can_admin, zsite_member_is_invite, zsite_member_new, ZSITE_MEMBER_STATE_ACTIVE
from model.po_review import po_review_get, po_review_new, po_review_show_list_with_user, po_review_count, po_review_list_by_zsite_id
from zkit.page import page_limit_offset
from model.user_auth import newbie_redirect, user_new_by_mail
from model.zsite_com_invite import zsite_member_invite, zsite_review_invite
from zkit.txt import EMAIL_VALID
from model.user_mail import user_id_by_mail


PAGE_LIMIT = 40

@urlmap('/review/admin')
@urlmap('/review/admin-(\d+)')
class ReviewAdmin(AdminBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)

        count = po_review_count(zsite_id)
        page, limit, offset = page_limit_offset(
            '/review/admin-%s',
            count,
            n,
            PAGE_LIMIT,
        )
        review_list = po_review_list_by_zsite_id(zsite_id, limit, offset)
        return self.render(
            can_admin=can_admin,
            review_list=review_list,
            page=page
        )

@urlmap('/review/admin/show')
class ReviewAdmin(AdminBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        review_list = po_review_show_list_with_user(zsite_id)
        return self.render(can_admin=can_admin, review_list=review_list)


def _invite_friend(self, mail_name_list):
    for mail, name in mail_name_list:
        mail = mail.strip().lower()
        name = name.strip()
        if EMAIL_VALID.match(mail):
            user_id = user_id_by_mail(mail)
            if not user_id:
                user = user_new_by_mail(mail, name=name)
                user_id = user.id

            zsite_review_invite(self.zsite, user_id, self.current_user)


@urlmap('/review/invite')
class ReviewInvite(LoginBase):
    def get(self):
        return self.render()

    def post(self):
        arguments = self.request.arguments
        self._invite_friend(zip(arguments['mail'], arguments['name']))
        return self.redirect('/review')

    _invite_friend = _invite_friend



@urlmap('/review')
class Review(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        review = po_review_get(zsite_id, current_user_id)
        self.render(can_admin=can_admin, review=review)

    def post(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        current_user = self.current_user

        name = self.get_argument('txt', '')
        po_review_new(zsite_id, current_user_id, name)

        if self.get_argument('join', None):
            if zsite_member_is_invite(zsite_id, current_user_id):
                zsite_member_new(zsite_id, current_user_id, ZSITE_MEMBER_STATE_ACTIVE)

        path = newbie_redirect(current_user)
        if path:
            return self.redirect(path)

        return self.get()

@urlmap('/review-(\d+)')
class ReviewPage(ZsiteBase):
    def get(self, n):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        if can_admin:
            return self.redirect('/review/admin')
        count = po_review_count(zsite_id)
        page, limit, offset = page_limit_offset(
            '/review-%s',
            count,
            n,
            PAGE_LIMIT,
        )
        review_list = po_review_list_by_zsite_id(zsite_id, limit, offset)
        self.render(can_admin=can_admin, page=page, review_list=review_list)

from ctrl.zsite.com.member import _invite_member

@urlmap('/review/admin/invite')
class ReviewAdminInvite(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id
        can_admin = zsite_member_can_admin(zsite_id, current_user_id)
        self.render(can_admin=can_admin)

    def post(self):
        arguments = self.request.arguments
        self._invite_friend( zip(arguments['mail_friend'], arguments['name_friend']) )
        self._invite_member( zip(arguments['mail_member'], arguments['name_member']) )
        self.get()

    _invite_friend = _invite_friend
    _invite_member = _invite_member
