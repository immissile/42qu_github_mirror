#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite,ZSITE_STATE_VERIFY 
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite_show import user_show_id_list, zsite_show_count

PAGE_LIMIT = 100

@urlmap('/user_list')
@urlmap('/user_list-(\d+)')
class Index(Base):
    def get(self, n=1):
        total = Zsite.where().count()
        page, limit, offset = page_limit_offset(
            href='/user_list-%s',
            total=total,
            n=n,
            limit=PAGE_LIMIT
        )
        user_list = Zsite.where().order_by('id desc')[offset:offset+limit]

        self.render(
            user_list=user_list,
            page=page,
        )


@urlmap('/user_show_id_list')
@urlmap('/user_show_id_list-(\d+)')
class IndexV(Base):
    def get(self, n=1):
        n = int(n)
        count = Zsite.raw_sql(
            "select max(id) from zsite where cid=%s and state=%s"%(
                CID_USER,
                ZSITE_STATE_VERIFY 
            )

        )
        page, limit, offset = page_limit_offset('/user_show_id_list-%s', count, n, 64)
        zsite_list = Zsite.where(cid=CID_USER).where("state>=%s"%ZSITE_STATE_VERIFY)[offset:offset+limit]
        self.render(zsite_list=zsite_list, page=page)
