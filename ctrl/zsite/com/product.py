#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.product import product_new, product_by_com_id, Product
from model.po import po_product_new
from job import AdminBase
import json
from zkit.jsdict import JsDict
from zkit.pic import picopen
from model.ico import site_ico_new, site_ico_bind
from zkit.pic import pic_fit_width_cut_height_if_large
from urlparse import urlparse



@urlmap('/product/new')
class ProductNew(AdminBase):
    def get(self):
        self.render()
    
    
    def post(self):
        user_id = self.current_user_id
        zsite = self.zsite

        arguments = self.request.arguments
        pro_url = arguments.get('pro_url',[])
        pro_name = arguments.get('pro_name',[])
        pro_bio = arguments.get('pro_bio',[])

        pros = None
        po_pre = None

        pros = zip(pro_url,pro_name,pro_bio)
        if pro_name:
            for pro_u,pro_n,pro_b in pros:
                po_pro = po_product_new(user_id,pro_n,pro_b,zsite.id)
        
                info_json = JsDict()
                info_json.name = pro_n
                info_json.pro_url = pro_u
                product_new(po_pro.id,info_json
                        )
            self.redirect('/product/new/%s'%'0')
        self.get()


def _product_save(self):
    current_user_id = self.current_user.id
    product_list = product_by_com_id(self.zsite.id)
    position = int(self.get_argument('position',0))
    origin = self.get_argument('origin',None)
    plan = self.get_argument('plan',None)
    pro_ot_name = self.get_arguments('pro_ot_name',None)
    pro_ot_url = self.get_arguments('pro_ot_url',None)
    same = self.get_argument('same',None)
    dist = self.get_argument('dist',None)
    advan = self.get_argument('advan',None)
    _product = self.get_argument('product',None)
    market = self.get_argument('market',None)
    team = self.get_argument('team',None)
    culture = self.get_argument('culture',None)
    money = self.get_argument('money',None)
    hope = self.get_argument('hope',None)
    pro_ot = zip(pro_ot_name,pro_ot_url)
    _pro = []
    if pro_ot:
        for pro in pro_ot:
            if pro[1] or pro[0]:
                if not pro[0]:
                    _pro.append([urlparse(pro[1]).netloc,pro[1]])
                else:
                    _pro.append([pro[0],pro[1]])
        pro_ot = _pro
    pic_id = None
    files = self.request.files
    if 'pic' in files:
        pic = files['pic'][0]['body']
        pic = picopen(pic)
        if pic:
            pic = pic_fit_width_cut_height_if_large(pic,215)
            pic_id = site_ico_new(current_user_id, pic)
    return product_list,position,origin,plan,pro_ot,same,dist,advan,_product,market,team,culture,money,hope,pic_id

@urlmap('/product/new/(\d+)')
class ProductNewN(AdminBase):
    def get(self,id=0):
        id = int(id)
        product_list = product_by_com_id(self.zsite.id)
        if id+1 > len(product_list):
            self.redirect('/job/new')
        position = self.get_argument('position',0)
        if not id:
            product_list = product_by_com_id(self.zsite.id)
        else:
            position = id
        self.render(product_list=product_list,position=position)


    _product_save = _product_save
    
    def post(self,id=0):
        id = int(id)
        product_list,position,origin,plan,pro_ot,same,dist,advan,_product,market,team,culture,money,hope,pic_id = self._product_save()
        product = product_list[id] or None
        
        if product:
            _info = JsDict(json.loads(product.info_json))
            _info.pic_id = pic_id
            _info.pro_ot = pro_ot
            _info.origin = origin
            _info.plan = plan
            _info.same = same
            _info.different = dist
            _info.advan = advan
            _info.product = _product
            _info.market = market
            _info.team = team
            _info.culture = culture
            _info.money = money
            _info.hope =hope
            product.info_json = json.dumps(dict(iter(_info)))
            product.save()



        if int(position)-1<len(product_list):
            return self.redirect('/product/new/%s'%(id+1))
        else:
            return self.redirect('/job/new')

@urlmap('/product/edit/(\d+)')
class ProductEdit(AdminBase):
    def get(self,id):
        product = None
        if id:
            product = Product.mc_get(id)
        if product:
            self.render(product=product)
        else:
            self.redirect('/')


    _product_save = _product_save
    
    
    def post(self,id):
        product_list,position,origin,plan,pro_ot,same,dist,advan,_product,market,team,culture,money,hope,pic_id = self._product_save()
        product = Product.mc_get(id)
        if product:
            _info = JsDict(json.loads(product.info_json))
            _info.pic_id = pic_id
            _info.pro_ot = pro_ot
            _info.origin = origin
            _info.plan = plan
            _info.same = same
            _info.different = dist
            _info.advan = advan
            _info.product = _product
            _info.market = market
            _info.team = team
            _info.culture = culture
            _info.money = money
            _info.hope =hope
            product.info_json = json.dumps(dict(iter(_info)))
            product.save()
        self.redirect('/')
