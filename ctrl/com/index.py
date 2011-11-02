# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.com import urlmap
from ctrl._util.site import _SiteListBase as _ComListBase, FavBase, MyBase
from model.cid import CID_COM
from model.zsite_com import zsite_com_count, zsite_com_list
from zkit.jsdict import JsDict

class ComListBase(_ComListBase):
    template = '/ctrl/com/index/index.htm'
    
    @property
    def user_id(self):
        return self.current_user_id

@urlmap('/')
@urlmap('/-(\d+)')
class Index(ComListBase, Base):
    page_url = '/-%s'

    def _total(self):
        return zsite_com_count(CID_COM)

    def _page_list(self,limit,offset):
        return zsite_com_list(CID_COM, limit, offset)


@urlmap('/new')
class New(Base):
    def get(self):
        self.render(errtip=JsDict())


    def post(self):
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

