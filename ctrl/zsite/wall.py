#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl.zsite._urlmap import urlmap
from model.reply import STATE_SECRET, STATE_ACTIVE
from model.wall import Wall
from model.reply import Reply
from zkit.page import page_limit_offset

PAGE_LIMIT = 42

def post_reply(self, reply_new=None):
    txt = self.get_argument('txt', None)
    if txt:
        secret = self.get_argument('secret', None)
        user_id = self.current_user_id
        reply = reply_new(
            user_id,
            txt,
            STATE_SECRET if secret else STATE_ACTIVE
        )


@urlmap('/wall')
class Index(LoginBase):
    def get(self):
        zsite = self.zsite
        self.redirect(zsite.link)

    def post(self):
        zsite = self.zsite
        link = zsite.link
        post_reply(self, zsite.reply_new)
        self.redirect(link)


@urlmap('/wall-(\-?\d+)')
class Page(ZsiteBase):
    def get(self, n):
        zsite = self.zsite
        zsite_link = zsite.link
        page, limit, offset = page_limit_offset(
            '%s/wall-%%s' % zsite_link,
            zsite.reply_total,
            n,
            PAGE_LIMIT
        )
        reply_list = zsite.reply_list_reversed(limit, offset)

        self.render(
            reply_list=reply_list,
            page=page
        )


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
        zsite_link = zsite.link

        wall = Wall.mc_get(id)

        if not wall:
            return self.redirect('/')

        zsite_id_list = wall.zsite_id_list()
        if zsite_id not in zsite_id_list:
            return self.redirect('/')

        page, limit, offset = page_limit_offset(
            '%s/wall/%s-%%s' % (zsite_link, id),
            wall.reply_total,
            n,
            PAGE_LIMIT
        )

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


@urlmap('/wall/reply/rm/(\d+)')
class ReplyRm(ZsiteBase):
    def post(self, id):
        current_user_id = self.current_user_id
        r = Reply.mc_get(id)
        can_rm = r.can_rm(current_user_id)

        wall = Wall.mc_get(r.rid)
        if r:
            zsite_id_list = wall.zsite_id_list()
            if wall:
                if can_rm is False and (current_user_id in zsite_id_list):
                    can_rm = True

        if can_rm:
            wall.reply_rm(r)
        self.finish({'success':can_rm})
