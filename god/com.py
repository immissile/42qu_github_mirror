#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.cid import CID_COM
from zkit.page import page_limit_offset
from model.zsite import Zsite
from model.po_product import product_list, product_count
from model.po_product_show import product_show_new, product_show_rm
from model.po import Po
PAGE_LIMIT = 48

@urlmap('/com')
@urlmap('/com-(\d+)')
class ComIndex(Base):
    def get(self, n=1):
        qs = Zsite.where(cid=CID_COM)
        total = qs.count()
        page, limit, offset = page_limit_offset(
                '/com-%s',
                total,
                n,
                PAGE_LIMIT,
                )
        li = qs.order_by('id desc')[offset: offset+limit]
        self.render(
                li=li,
                page=page
                )

@urlmap('/com/(\d+)')
@urlmap('/com/(\d+)-(\d+)')
class ComPage(Base):
    def get(self, state, n=1):
        state = int(state)
        qs = Zsite.where(cid=CID_COM)
        total = qs.count()
        page, limit, offset = page_limit_offset(
                '/com/%s-%%s'%state,
                total,
                n,
                PAGE_LIMIT,
                )
        li = qs.order_by('id desc')[offset:offset+limit]
        self.render(
                state=state,
                li=li,
                page=page
                )

@urlmap('/product/show/rm/(\d+)')
class ProductShowRm(Base):
    def get(self, id):
        po = Po.mc_get(id)
        product_show_rm(po)
        return self.redirect("/product") 

@urlmap('/product/show/new/(\d+)')
class ProductShowNew(Base):
    def get(self, id):
        po = Po.mc_get(id)
        product_show_new(po)
        return self.redirect("/product") 

@urlmap('/product-(\d+)')
class Product(Base):
    def get(self, n=1):
        count = product.count()
        page, limit, offset = page_limit_offset(
            '/product-%s',
            count,
            n,
            PAGE_LIMIT,
        )
        li = product_list(limit, offset)
        self.render(
            li = li,
            page=str(page)
        )



