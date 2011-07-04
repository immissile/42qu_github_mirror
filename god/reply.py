#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.reply import Reply
from zkit.page import page_limit_offset
from model.txt import txt_bind
from model.po import Po
PAGE_LIMIT = 50

@urlmap('/reply_list/(\d+)(?:-(\d+))?')
class ReplyList(Base):
    def get(self, cid, n=1):
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
        Po.mc_bind(li, 'po', 'rid')
        self.render(
            reply_list=li,
            page=page,
        )



@urlmap('/reply/rm/(\d+)')
class ReplyRm(Base):
    def get(self, id):
        r = Reply.mc_get(id)
        if r:
            r.rm()
            self.finish('Y')
        else:
            self.finish('N')
