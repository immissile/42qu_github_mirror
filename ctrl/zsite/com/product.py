#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from model.product import product_new, product_by_com_id
from model.po import po_product_new
from job import AdminBase
import json
from zkit.jsdict import JsDict
from zkit.pic import picopen
from model.ico import site_ico_new, site_ico_bind

@urlmap('/product/new')
class ProductNew(AdminBase):
    def get(self):
        self.render()
    
    
    def post(self):
        user_id = self.current_user_id
        zsite = self.zsite
        pro_url = self.get_arguments('pro_url',None)
        pro_name = self.get_arguments('pro_name',None)
        pro_bio = self.get_arguments('pro_bio',None)
        pros = None
        po_pre = None

        if pro_url and pro_name and pro_bio:
            pros = zip(pro_url,pro_name,pro_bio)
        if pros:
            for pro_u,pro_n,pro_b in pros:
                po_pro = po_product_new(user_id,pro_n,pro_b,zsite.id)
        
                info_json = JsDict()
                info_json.name = pro_n
                info_json.pro_url = pro_u
                product_new(po_pro.id,info_json
                        )
            self.redirect('/product/new/%s'%'0')
        self.get()

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
            print position
        self.render(product_list=product_list,position=position)



    def post(self,id=0):
        id = int(id)
        current_user = self.current_user
        current_user_id = current_user.id
        product_list = product_by_com_id(self.zsite.id)
        position = int(self.get_argument('position',0))
        origin = self.get_argument('origin',None)
        plan = self.get_argument('plan',None)
        pro_ot_name = self.get_arguments('pro_ot_name',None)
        pro_ot_url = self.get_arguments('pro_ot_url',None)
        same = self.get_argument('same',None)
        dist = self.get_argument('dist',None)
        advan = self.get_argument('advan',None)
        product = self.get_argument('product',None)
        market = self.get_argument('market',None)
        team = self.get_argument('team',None)
        culture = self.get_argument('culture',None)
        money = self.get_argument('money',None)
        hope = self.get_argument('hope',None)

        files = self.request.files
        product = product_list[id] or None
        if product:
            _info = JsDict(json.loads(product.info_json))


            if 'pic' in files:
                pic = files['pic'][0]['body']
                pic = picopen(pic)
                if pic:
                    pic_id = site_ico_new(current_user_id, pic)
                    _info.pic_id = pic_id
            pro_ot = zip(pro_ot_name,pro_ot_url)
            
            _info.pro_ot = pro_ot
            _info.origin = origin
            _info.plan = plan
            _info.same = same
            _info.different = dist
            _info.advan = advan
            _info.product = product
            _info.market = market
            _info.team = team
            _info.culture = culture
            _info.money = money
            _info.hope =hope
            product.info = _info
            product.save()



        print len(product_list),position
        if int(position)-1<len(product_list):
            return self.redirect('/product/new/%s'%(id+1))
        else:
            return self.redirect('/job/new')

