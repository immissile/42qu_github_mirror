# -*- coding: utf-8 -*-
from _handler import Base, LoginBase
from ctrl._urlmap.com import urlmap
from ctrl._util.site import _SiteListBase as _ComListBase, MyBase
from model.cid import CID_COM
from model.zsite_com import zsite_com_count, com_new, zsite_com_place_new
from model.ico import site_ico_new, site_ico_bind
from zkit.jsdict import JsDict
from model.motto import motto_set
from model.txt import txt_new
from model.zsite_url import url_by_id, url_new, url_valid, RE_URL
from zkit.pic import picopen
from zkit.errtip import Errtip
from model.zsite_member import zsite_member_new, ZSITE_MEMBER_STATE_ACTIVE
from model.po_product_show import product_show_list
from model.zsite_show import zsite_show_list, zsite_show_count
from model.zsite_member import zsite_list_by_member_admin
from model.zsite_member import zsite_id_list_by_member_admin
from model.zsite_com import zsite_com_new

@urlmap('/com/list')
@urlmap('/com/list-(\d+)')
class ComList(_ComListBase, Base):
    template = '/ctrl/com/index/com_list.htm'

    @property
    def user_id(self):
        return self.current_user_id
    page_url = '/com/list-%s'

    def _total(self):
        return zsite_show_count(CID_COM)

    def _page_list(self, limit, offset):
        return zsite_show_list(CID_COM, limit, offset)

@urlmap('/')
class Index(Base):
    def get(self):
        self.render(product_list=product_show_list())

@urlmap('/mine')
class Mine(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        com_list = zsite_list_by_member_admin(current_user_id)
        self.render(com_list=com_list)



@urlmap('/product')
class Product(Base):
    def get(self):
        self.render(product_list=product_all())


@urlmap('/new')
class ComNew(LoginBase):
    def get(self):
        self.render(errtip=JsDict())


    def post(self):
        errtip = Errtip()
        current_user = self.current_user
        current_user_id = current_user.id
        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        url = self.get_argument('url', None)
        pid = self.get_arguments('pid', None)
        address = self.get_arguments('address', None)
        phone = self.get_argument('phone', None)
        pid_add = zip(pid, address)

        if not name:
            errtip.name = '请输入名称'

        if not motto:
            errtip.motto = '请编写签名'


        if url:
            errtip.url = url_valid(url)

        files = self.request.files
        pic_id = None

        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                pic_id = site_ico_new(current_user_id, pic)
            else:
                errtip.pic = '图片格式有误'
        else:
            pic_id = self.get_argument('pic_id', None)
            if not pic_id:
                errtip.pic = '请上传图片'

        if not errtip:
            com = com_new(name, current_user_id )
            com_id = com.id
            zsite_com_new(com_id, phone=phone)
            site_ico_bind(current_user_id, pic_id, com_id)
            motto_set(com_id, motto)
            zsite_member_new(com_id, current_user_id, state=ZSITE_MEMBER_STATE_ACTIVE)
            if pid_add:
                for pa in pid_add:
                    zsite_com_place_new(com_id, int(pa[0]), pa[1])
            else:
                pid_add = self.get_argument('pid_add', None)
            if url:
                url_new(com_id, url)
            return self.redirect('%s/product/new'%com.link)


        return self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            url=url,
            #txt=txt,
            phone=phone,
            pic_id=pic_id,
            pid_add=pid_add
        )

