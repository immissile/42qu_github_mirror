#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from zkit.page import page_limit_offset
from zweb._urlmap import urlmap
from model.cid import CID_ZSITE
from model.follow import follow_rm, follow_new, follow_count_by_to_id, follow_id_list_by_to_id, follow_id_list_by_from_id_cid
from model.zsite import Zsite

PAGE_LIMIT = 42

@urlmap('/follow')
class Follow(XsrfGetBase):
    def get(self):
        current_user = self.current_user
        zsite_id = self.zsite_id
        follow_new(current_user.id, zsite_id)
        self.render()

@urlmap('/follow/rm')
class Unfollow(XsrfGetBase):
    def get(self):
        current_user = self.current_user
        zsite_id = self.zsite_id
        follow_rm(current_user.id, zsite_id)
        self.redirect('/')

@urlmap('/follower')
@urlmap('/follower/(\d+)')
class Follower(Base):
    def get(self, n=1):
        zsite_id = self.zsite_id
        page, limit, offset = page_limit_offset(
            '/follower/%s',
            follow_count_by_to_id(zsite_id),
            n,
            PAGE_LIMIT
        )
        ids = follow_id_list_by_to_id(zsite_id, limit, offset)
        if type(n) == str and not ids:
            return self.redirect('/follower')

        follower = Zsite.mc_get_list(ids)
        self.render(
            follower=follower,
            page=page,
        )

@urlmap('/following/(\d)')
@urlmap('/following/(\d)/(\d+)')
class Following(Base):
    def get(self, cid, n=1):
        cid = int(cid)
        if cid not in CID_ZSITE:
            return self.redirect('/')

        zsite_id = self.zsite_id
        ids = follow_id_list_by_from_id_cid(zsite_id, cid)
        page, limit, offset = page_limit_offset(
            '/following/%s/%%s' % cid,
            len(ids),
            n,
            PAGE_LIMIT
        )
        ids = ids[offset: offset + limit]
        if type(n) == str and not ids:
            return self.redirect('/following/%s' % cid)

        following = Zsite.mc_get_list(ids)
        self.render(
            cid=cid,
            following=following,
            page=page,
        )
