#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.rss import rss_po_list_by_state, RssPo, RSS_UNCHECK, RSS_PRE_PO, RSS_RM, rss_po_total, get_rss_by_gid, rss_total_gid, RSS_RT_PO, Rss, rss_new, mail_by_rss_id
from zkit.page import page_limit_offset
from model.zsite import Zsite
from model.site_sync import site_sync_rm, site_sync_new
from model.zsite import zsite_by_query, Zsite
from zkit.algorithm.unique import unique
from urlparse import parse_qs, urlparse

PAGE_LIMIT = 50

@urlmap('/rss_index')
@urlmap('/rss_index/(\d+)')
@urlmap('/rss_index/(\d+)-(\-?\d+)')
class RssIndex(Base):
    def get(self, state=RSS_UNCHECK, n=1):
        total = rss_po_total(state)

        page, limit, offset = page_limit_offset(
                 '/rss_index/%s-%%s'%state,
                 total,
                 n,
                 PAGE_LIMIT
             )
        rss_po_list = rss_po_list_by_state(state, limit, offset)
        self.render(
                rss_po_list=rss_po_list,
                page=page,
                rss_state=state
            )

    def post(self, state=RSS_UNCHECK, n=1):
        ids = self.get_argument('id').split()
        if ids:
            for id in ids:
                rss = RssPo.mc_get(id)
                if rss and rss.state == RSS_UNCHECK:
                    rss.state = RSS_RM
                    rss.save()
        self.get()


@urlmap('/rss/rm/(\d+)')
class RssRm(Base):
    def get(self, id):
        pre = RssPo.mc_get(id)
        if pre:
            pre.state = RSS_RM
            pre.save()
        self.redirect('/rss_index')

@urlmap('/rss/gid')
@urlmap('/rss/gid/(\-?\d+)')
@urlmap('/rss/gid/(\-?\d+)-(\d+)')
class RssGid(Base):
    def get(self, gid=0, n=1):
        gid = int(gid)
        total = rss_total_gid(gid)
        page, limit, offset = page_limit_offset(
                '/rss/gid/%s-%%s'%gid,
                total,
                n,
                PAGE_LIMIT
                )
        rss_list = get_rss_by_gid(gid, limit, offset)
        self.render(
                rss=rss_list,
                page=page
                )

@urlmap('/rss/gid/edit/(\d+)')
class RssGidEdit(Base):
    def get(self, id):
        rss = Rss.mc_get(id)
        next = self.request.headers.get('Referer', '')
        self.render(rss=rss,
                next=next)

    def post(self, id):
        rss = Rss.mc_get(id)
        next = self.get_argument('next', None) or '/rss_index'
        url = self.get_argument('url', None)
        link = self.get_argument('link', None)
        user_id = self.get_argument('user_id', None)
        name = self.get_argument('name', None)

        if url:
            rss.url = url

        if link:
            rss.link = link

        if name:
            rss.name = name

        if user_id:
            rss.user_id = user_id

        rss.save()

        self.redirect(next)


@urlmap('/rss/new')
class RssNew(Base):
    def get(self):
        next = self.request.headers.get('Referer', '')
        self.render('/god/rss/rss_gid_edit.htm', next=next)

    def post(self):
        next = self.get_argument('next', None) or '/rss_index'
        url , link , user_id , name , auto = _rss_post_argument(self)
        if url and user_id:
            rss = rss_new(user_id, url, name, link, auto=1)
            self.redirect(next)
        else:
            self.get()



def _rss_post_argument(self):
    url = self.get_argument('url', None)
    link = self.get_argument('link', None)
    user_id = self.get_argument('user_id', None)
    name = self.get_argument('name', None)
    auto = self.get_argument('auto', None)

    user = Zsite.mc_get(user_id)
    if not user:
        user_id = 0

    return url , link , user_id , name , auto


@urlmap('/rss/gid/rm/(\d+)')
class RssGid(Base):
    def get(self, id):
        id = int(id)
        rss = Rss.mc_get(id)

        if not rss.gid:
            rss.delete()

        if rss.gid > 0:
            rss.gid = -rss.gid
            rss.save()

        self.redirect('/rss/gid/1')


@urlmap('/rss/edit')
@urlmap('/rss/edit/(\d+)')
class RssEdit(Base):
    def get(self, id=0):
        if id:
            id = int(id)
            rss = Rss.mc_get(id)
            self.render(rss=rss)
        else:
            self.render()

    def post(self):
        url , link , user_id , name , auto = _rss_post_argument(self)

        rss = Rss.mc_get(id)
        if rss:
            if url:
                rss.url = url

            if link:
                rss.link = link

            if user_id:
                rss.user_id = user_id

            if name:
                rss.name = name

            rss.auto = int(bool(auto))

            rss.save()


@urlmap('/rss/po/edit/(\d+)')
class RssPoEdit(Base):
    def get(self, id):
        next = self.request.headers.get('Referer', '')
        po = RssPo.get(id)
        self.render(next=next, po=po)

    def post(self, id):
        id = int(id)
        txt = self.get_argument('txt', None)
        rt = self.get_argument('rt', None)
        title = self.get_argument('name', None)
        sync = self.get_argument('sync', None)
        po = RssPo.mc_get(id)
        po.txt = txt
        next = self.get_argument('next', None) or '/rss_index'
        if rt:
            po.state = RSS_RT_PO
        else:
            po.state = RSS_PRE_PO
        site = self.get_argument('site', None)
        if site:
            po.site_id = site
        if title:
            po.title = title
        po.save()

        if sync:
            site_sync_new(id)
        else:
            site_sync_rm(id)

        self.redirect(next)


@urlmap('/rss/mail/(\d+)')
class RssMail(Base):
    def get(self, id):
        if id:
            mail_by_rss_id(id)
        next = self.request.headers.get('Referer', None) or '/rss_index'
        self.redirect(next)


@urlmap('/rss/add')
class RssAdd(Base):
    def get(self):
        self.render()

    def post(self):
        user_list = self.get_argument('user_list')
        user_list = filter(bool, map(str.strip, user_list.splitlines()))

        user_list_exist = []
        user_list_not_exist = []

        for i in user_list:
            zsite_id = zsite_by_query(i)
            if zsite_id:
                user_list_exist.append(zsite_id)
            else:
                user_list_not_exist.append(i)

        user_list_not_exist = unique(user_list_not_exist)
        user_list_exist = unique(user_list_exist)

        self.render(
            user_list_exist=Zsite.mc_get_list(user_list_exist),
            user_list_not_exist=user_list_not_exist,
        )


@urlmap('/rss/bind')
class RssBind(Base):
    def post(self):
        arguments = parse_qs(self.request.body, True)

        link = ''
        name = ''
        auto = 1

        user_list_exist = []
        for txt, id in zip(arguments.get('txt'), arguments.get('id')):
            user_id = int(id)

            for url in txt.splitlines():
                url = url.strip()
                rss = rss_new(user_id, url, name, link, auto)

            user_list_exist.append(user_id)
 
        if user_list_exist:
            self.render(
                '/god/rss/rss_add.htm',
                user_list_exist=Zsite.mc_get_list(user_list_exist),
                user_list_not_exist=[],
                success = True
            )
        else:
            self.rediect("/rss/add")

