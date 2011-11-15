#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.product import product_new, product_by_com_id, Product
from model.po import po_product_new
from _handler import AdminBase
import json
from zkit.jsdict import JsDict
from zkit.pic import picopen
from model.ico import site_ico_new, site_ico_bind
from zkit.pic import pic_fit_width_cut_height_if_large
from urlparse import urlparse
from model.po_pic import product_pic_new
from model.po import po_id_list_by_com_id

@urlmap('/product/new')
class ProductNew(AdminBase):
    def get(self):
        self.render()
    
    
    def post(self):
        user_id = self.current_user_id
        zsite = self.zsite

        arguments = self.request.arguments

        pro_url = arguments.get('pro_url')
        pro_name = arguments.get('pro_name')
        pro_bio = arguments.get('pro_bio')


        pros = zip(pro_url,pro_name,pro_bio)
        pros = filter(lambda p:p[1]is not '',pros)
        if pros:
            for pro_u,pro_n,pro_b in pros:
                print pros,'!!'
                po_pro = po_product_new(user_id,pro_n,pro_b,zsite.id)
                info_json = JsDict()
                info_json.pro_url = pro_u
                p = product_new(po_pro.id,info_json)
            pos = po_id_list_by_com_id(zsite.id)
            self.redirect('/product/new/%s'%pos[0])
        self.get()


def _product_save(self,product):
    current_user_id = self.current_user.id
    position = int(self.get_argument('position',0))
    origin = self.get_argument('origin',None)
    plan = self.get_argument('plan',None)
    similar_product_name = self.get_arguments('similar_product_name',None)
    similar_product_url = self.get_arguments('similar_product_url',None)
    same = self.get_argument('same',None)
    different = self.get_argument('different',None)
    advantage = self.get_argument('advantage',None)
    _product = self.get_argument('product',None)
    market = self.get_argument('market',None)
    pro_ot = zip(similar_product_name,similar_product_url)
    _pro = []
    if pro_ot:
        for _name,_url in pro_ot:
            if _name or _url:
                if not _name:
                    _pro.append([urlparse(_url).netloc,_url])
                else:
                    _pro.append([_name,_url])
        pro_ot = _pro
    pic_id = None
    files = self.request.files
    if product:
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                pic_id = product_pic_new(self.zsite_id, product.id,pic)
        
        _info = JsDict(json.loads(product.info_json))
        _info.pic_id = pic_id
        _info.pro_ot = pro_ot
        _info.origin = origin
        _info.plan = plan
        _info.same = same
        _info.different = different
        _info.advantage = advantage
        _info.product = _product
        _info.market = market
        product.info_json = json.dumps(dict(iter(_info)))
        product.save()

@urlmap('/product/new/(\d+)')
class ProductNewN(AdminBase):
    def get(self,id):
        id = int(id)
        product_list = product_by_com_id(self.zsite.id)
        product = Product.mc_get(id)
        if product:
            if product_list.index(product) > len(product_list):
                self.redirect('/job/new')
            product_list = product_by_com_id(self.zsite.id)
            return self.render(product_list=product_list,product=product,com_id=self.zsite.id,position=1)
        self.redirect('/')

    _product_save = _product_save
    
    def post(self,id=0):
        product_list = product_by_com_id(self.zsite.id)
        id = int(id)
        product = Product.mc_get(id)
        if product:
            self._product_save(product)

            if product_list.index(product) <len(product_list):
                return self.redirect('/product/new/%s'%(product_list[product_list.index(product)+1].id))
            else:
                return self.redirect('/job/new')
        self.redirect('/')

@urlmap('/product/edit/(\d+)')
class ProductEdit(AdminBase):
    def get(self,id):
        product = None
        if id:
            product = Product.mc_get(id)
        if product:
            self.render(product=product,com_id=self.zsite.id)
        else:
            self.redirect('/')


    _product_save = _product_save
    
    
    def post(self,id):
        product = Product.mc_get(id)
        self._product_save(product)
        self.redirect('/')
