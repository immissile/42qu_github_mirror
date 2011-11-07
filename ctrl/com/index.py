# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.com import urlmap
from ctrl._util.site import _SiteListBase as _ComListBase, FavBase, MyBase
from model.cid import CID_COM
from model.zsite_com import zsite_com_count, zsite_com_list, com_new, zsite_com_place_new
from model.ico import site_ico_new, site_ico_bind
from zkit.jsdict import JsDict
from model.motto import motto_set
from model.txt import txt_new
from model.zsite_url import url_by_id, url_new, url_valid, RE_URL
from zkit.pic import picopen
from zkit.errtip import Errtip


class ComListBase(_ComListBase,Base):
    template = '/ctrl/com/index/index.htm'
    
    @property
    def user_id(self):
        return self.current_user_id

@urlmap('/')
@urlmap('/-(\d+)')
class Index(ComListBase):
    page_url = '/-%s'

    def _total(self):
        return zsite_com_count(CID_COM)

    def _page_list(self,limit,offset):
        return zsite_com_list(CID_COM, limit, offset)

@urlmap('/job')
class Job(Base):
    def get(self):
        self.finish('it"s jobs')


@urlmap('/product')
class Product(Base):
    def get(self):
        self.render()

@urlmap('/new')
class New(Base):
    def get(self):
        self.render(errtip=JsDict())


    def post(self):
        errtip = Errtip()
        current_user = self.current_user
        current_user_id = current_user.id
        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        url = self.get_argument('url', None)
        #txt = self.get_argument('txt', None)
        pid = self.get_arguments('pid', None)
        address = self.get_arguments('address',None)
        pid_add = zip(pid,address)
        
        print pid,'!!!!!',address
        print pid_add,'!!!!!!!!'
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
            site_ico_bind(current_user_id, pic_id, com_id)
            motto_set(com_id, motto)
            #txt_new(com_id, txt)
            if pid_add:
                for pa in pid_add:
                    zsite_com_place_new(com_id,int(pa[0]),pa[1])
            if url:
                url_new(com_id, url)
            self.redirect(com.link)
            return


        return self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            url=url,
            #txt=txt,
            pic_id=pic_id
        )

