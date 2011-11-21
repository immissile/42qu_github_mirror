#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
import json
from zkit.jsdict import JsDict
from zkit.pic import picopen
from model.ico import site_ico_new, site_ico_bind
from zkit.pic import pic_fit_width_cut_height_if_large
from urlparse import urlparse
from model.po_pic import product_pic_new
from model.po_product import Po, po_product_new, po_product_update, product_id_list_by_com_id, product_rm

@urlmap('/product/new')
class ProductNew(AdminBase):
    def get(self):
        self.render()


    def post(self):
        user_id = self.current_user_id
        zsite = self.zsite

        arguments = self.request.arguments

        product_url = arguments.get('product_url')
        product_name = arguments.get('product_name')
        product_about = arguments.get('product_about')


        pros = zip(product_url, product_name, product_about)
        pros = filter(lambda p : p[1] is not '', pros)
        if pros:
            for url, name, about in pros:
                info_json = JsDict()
                info_json.product_url = url
                info_json.product_about = about
                po_product_new(user_id, name, info_json, zsite.id)

            next_id = product_id_list_by_com_id(zsite.id)[0]
            return self.redirect('/product/new/%s'%next_id)

        self.get()


def _product_save(self, product):
    current_user_id = self.current_user_id
    if not product.can_admin(current_user_id): 
        return
    #TODO ! 判断current_user_id 是不是有com的管理权限
    if 0:
        return

    position = int(self.get_argument('position', 0))
    origin = self.get_argument('origin', None)
    plan = self.get_argument('plan', None)
    similar_product_name = self.get_arguments('similar_product_name', None)
    similar_product_url = self.get_arguments('similar_product_url', None)
    same = self.get_argument('same', None)
    different = self.get_argument('different', None)
    advantage = self.get_argument('advantage', None)
    _product = self.get_argument('product', None)
    market = self.get_argument('market', None)

    product_similar = zip(similar_product_name, similar_product_url)
    _pro = []
    if product_similar:
        for _name, _url in product_similar:
            if _name or _url:
                if not _name:
                    _pro.append([urlparse(_url).netloc or _url, _url])
                else:
                    _pro.append([_name, _url])
        product_similar = _pro

    pic_id = None
    files = self.request.files
    if product:
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                pic_id = product_pic_new(self.zsite_id, product.id, pic)

        _info = JsDict(json.loads(product.txt or '{}'))
        _info.pic_id = pic_id
        _info.product_similar = product_similar
        _info.origin = origin
        _info.plan = plan
        _info.same = same
        _info.different = different
        _info.advantage = advantage
        _info.product = _product
        _info.market = market
        product.txt_set(json.dumps(dict(iter(_info))))
        product.save()

@urlmap('/product/new/(\d+)')
class ProductNewN(AdminBase):
    def get(self, id):
        id = int(id)
        product_list = product_id_list_by_com_id(self.zsite.id)
        product = Po.mc_get(id)
        if product:
            if id not in product_list:
                self.redirect('/job/new')

            return self.render(
                        product_list=Po.mc_get_list(product_list), 
                        product=product, 
                        com_id=self.zsite.id, 
                        position=1
                   )
        self.redirect('/')

    _product_save = _product_save

    def post(self, id=0):
        product_list = product_id_list_by_com_id(self.zsite.id)
        id = int(id)
        product = Po.mc_get(id)
        if product:
            self._product_save(product)

            if product_list[-1] != id:
                return self.redirect('/product/new/%s'%(product_list[product_list.index(id)+1]))
            else:
                return self.redirect('/job/new')

        self.redirect('/')

@urlmap('/product/edit/(\d+)')
class ProductEdit(AdminBase):
    def get(self, id):
        product = None
        if id:
            product = Po.mc_get(id)
        if product:
            self.render(product=product, com_id=self.zsite.id)
        else:
            self.redirect('/')


    _product_save = _product_save


    def post(self, id):
        product = Po.mc_get(id)
        self._product_save(product)
        self.redirect('/')

@urlmap('/product/rm/(\d+)')
class ProductRm(AdminBase):
    def get(self, id):
        if id:
            po_rm(self.current_user_id, id)
            self.redirect('/')
