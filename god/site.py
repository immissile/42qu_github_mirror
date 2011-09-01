#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.cid import CID_SITE
from model.zsite import Zsite, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE, ZSITE_STATE_VERIFY, zsite_rm_site
from zkit.page import page_limit_offset


@urlmap('/site_verify')
class SiteVerify(Base):
    def get(self):
        li = Zsite.where(cid=CID_SITE, state=ZSITE_STATE_APPLY).order_by('id')[:1]
        if li:
            self.render(site=li[0])
        else:
            self.redirect('/site')


@urlmap('/site')
@urlmap('/site-(\d+)')
class SiteList(Base):
    def get(self, n=1):
        qs = Zsite.where(cid=CID_SITE, state=ZSITE_STATE_ACTIVE)
        page, limit, offset = page_limit_offset(
            '/site-%s',
            qs.count(),
            n,
            50,
        )
        li = qs.order_by('id desc')[offset: limit+offset]
        self.render(
            li=li,
            page=page,
        )


@urlmap('/site/(\d+)')
class Site(Base):
    def get(self, id):
        o = Zsite.mc_get(id)
        if o and o.cid == CID_SITE:
            self.render(site=o)


@urlmap('/site/ok/(\d+)')
class SiteOk(Base):
    def get(self, id):
        o = Zsite.mc_get(id)
        if o and o.cid == CID_SITE:
            o.state = ZSITE_STATE_ACTIVE
            o.save()
        self.redirect('/site/%s' % id)


@urlmap('/site/rm/(\d+)')
class SiteRm(Base):
    def get(self, id):
        o = Zsite.mc_get(id)
        zsite_rm_site(id)
        self.redirect('/site/%s' % id)
