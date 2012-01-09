#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.reply import Reply
from zkit.page import page_limit_offset
from model.zsite import Zsite
from model.txt import txt_bind
from model.po import Po
from model.cid import CID_USER
from model.wall import Wall
PAGE_LIMIT = 50

@urlmap('/reply_list/(\d+)(?:-(\d+))?')
class ReplyList(Base):
    def get(self, cid, n=1):
        cid = int(cid)
        qs = Reply.where('cid = %s', cid)
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/reply_list/%s-%%s'%cid,
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        txt_bind(li)
        #print cid == CID_USER
        if cid == CID_USER:
            Wall.mc_bind(li, 'wall', 'rid')
            wall_list = [i.wall for i in li]
            Zsite.mc_bind(wall_list, 'from_user', 'from_id')
            Zsite.mc_bind(wall_list, 'to_user', 'to_id')
        else:
            Po.mc_bind(li, 'po', 'rid')

        Zsite.mc_bind(li, 'user', 'user_id')
        self.render(
            reply_list=li,
            page=page,
        )


@urlmap('/rm/reply/(\d+)')
class ReplyRm(Base):
    def get(self, id):
        r = Reply.mc_get(id)
        if r:
            r.rm()
        self.finish('{}')
