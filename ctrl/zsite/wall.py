#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, login
from ctrl._urlmap.zsite import urlmap
from model.reply import STATE_SECRET, STATE_ACTIVE
from model.wall import Wall
from model.reply import Reply
from zkit.page import page_limit_offset
from model.buzz_at import buzz_at_count,buzz_at_list
from model.zsite import Zsite
from model.cid import CID_SITE

PAGE_LIMIT = 42

def post_reply(self, reply_new=None):
    txt = self.get_argument('txt', None)
    if txt:
        secret = self.get_argument('secret', None)
        user = self.current_user
        reply = reply_new(
            user,
            txt,
            STATE_SECRET if secret else STATE_ACTIVE
        )
        return reply

@urlmap('/wall')
@urlmap('/wall-(\-?\d+)')
class Page(ZsiteBase):
    def get(self, n=1):
        zsite = self.zsite
        zsite_url = zsite.link
        total = zsite.reply_count

        page, limit, offset = page_limit_offset(
            '%s/wall-%%s' % zsite_url,
            total,
            n,
            PAGE_LIMIT
        )

        reply_list = zsite.reply_list_reversed(limit, offset)

        self.render(
            reply_list=reply_list,
            page=page
        )

    def post(self):
        zsite = self.zsite
        link = zsite.link
        post_reply(self, zsite.reply_new)
        self.redirect('%s/wall'%link)


@urlmap('/wall/reply2txt/(\d+)')
class Reply2Txt(ZsiteBase):
    def get(self, id):
        link = '/'
        reply = Reply.mc_get(id)
        if reply:
            link = '/wall/%s'%reply.rid

        self.redirect(link, True)


@urlmap('/wall/(\d+)')
@urlmap('/wall/(\d+)-(\d+)')
class Txt(ZsiteBase):
    def get(self, id, n=1):
        zsite = self.zsite
        zsite_id = zsite.id
        zsite_url = zsite.link
        current_user_id = self.current_user_id

        wall = Wall.mc_get(id)

        if not wall:
            return self.redirect('/')

        zsite_id_list = wall.zsite_id_list()
        if zsite_id not in zsite_id_list:
            return self.redirect('/')
        else:
            other = wall.zsite_other(zsite_id)
            if other.cid == CID_SITE or zsite_id == current_user_id:
                return self.redirect('%s/wall/%s'%(other.link, id))


        total = wall.reply_count
        page, limit, offset = page_limit_offset(
            '%s/wall/%s-%%s' % (zsite_url, id),
            total,
            n,
            PAGE_LIMIT
        )
        if type(n) == str and offset >= total:
            return self.redirect(zsite_url)

        reply_list = wall.reply_list_reversed(limit, offset)

        self.render(
            wall=wall,
            zsite_id_list=zsite_id_list,
            reply_list=reply_list,
            page=page
        )

    @login
    def post(self, id):
        wall = Wall.mc_get(id)
        post_reply(self, wall.reply_new)
        self.redirect('/wall/%s' % id)


@urlmap('/wall/rm/reply/(\d+)')
class ReplyRm(ZsiteBase):
    def post(self, id):
        current_user_id = self.current_user_id
        r = Reply.mc_get(id)
        can_admin = r.can_admin(current_user_id)

        wall = Wall.mc_get(r.rid)
        if r:
            zsite_id_list = wall.zsite_id_list()
            if wall:
                if can_admin is False and (current_user_id in zsite_id_list):
                    can_admin = True

        if can_admin:
            wall.reply_rm(r)
        self.finish({'success':can_admin})

