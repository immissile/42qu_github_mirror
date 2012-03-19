#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase
from zkit.page import page_limit_offset
from ctrl._urlmap.zsite import urlmap
from model.cid import CID_ZSITE_TUPLE, CID_SITE
from model.follow import follow_count_by_to_id, follow_id_list_by_to_id, follow_id_list_by_from_id, follow_id_list_by_from_id_cid
from model.zsite import Zsite
from model.zsite_fav import zsite_fav_list, zsite_fav_count_by_zsite

PAGE_LIMIT = 64


@urlmap('/follower')
@urlmap('/follower-(\d+)')
class Follower(ZsiteBase):
    def get(self, n=1):
        zsite_id = self.zsite_id
        zsite = self.zsite

        if zsite.cid == CID_SITE:
            title = '收藏'
            total = zsite_fav_count_by_zsite(zsite)
        else:
            title = '围观'
            total = follow_count_by_to_id(zsite_id)

        page, limit, offset = page_limit_offset(
            '/follower-%s',
            total,
            n,
            PAGE_LIMIT
        )

        if type(n) == str and offset >= total:
            return self.redirect('/follower')


        if zsite.cid == CID_SITE:
            zsite_list = zsite_fav_list(zsite, limit, offset)
        else:
            ids = follow_id_list_by_to_id(zsite_id, limit, offset)
            zsite_list = Zsite.mc_get_list(ids)

        self.render(
            '/ctrl/zsite/follow/_base.htm',
            zsite_list=zsite_list,
            page=page,
            title=title,
            path='/follower'
        )

@urlmap('/following(\d)?')
@urlmap('/following(\d)?-(\d+)')
class Following(ZsiteBase):
    def get(self, cid=0, n=1):
        if cid:
            cid = int(cid)
            if cid not in CID_ZSITE_TUPLE:
                return self.redirect('/following')

        zsite_id = self.zsite_id
        if cid:
            id_list = follow_id_list_by_from_id_cid(zsite_id, cid)
        else:
            id_list = follow_id_list_by_from_id(zsite_id)
        total = len(id_list)
        page, limit, offset = page_limit_offset(
            '/following%s-%%s' % (cid or ''),
            total,
            n,
            PAGE_LIMIT
        )
        if type(n) == str and offset >= total:
            return self.redirect('/following%s' % (cid or ''))

        id_list = id_list[offset: offset + limit]
        following = Zsite.mc_get_list(id_list)

        self.render(
            zsite_list=following,
            page=page,
            title='关注',
            path='/following%s'%(cid or '')
        )

