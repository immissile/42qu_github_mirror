# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from model.zsite import zsite_new_site, ZSITE_STATE_VERIFY
from zkit.txt import cnenlen

@urlmap('/new')
class SiteNew(LoginBase):
    def get(self):
        self.render(
            errtip=JsDict(),
        )

    def post(self):
        current_user_id = self.current_user_id
        current_user = self.current_user

        errtip = Errtip()
        name = self.get_argument('name', None)
        url = self.get_argument('url', None)
        site = None
        
        if not name:
            errtip.name = '请输入名称'
        elif cnenlen(name) > 18:
            errtip.name = '请不要超过九个汉字'
        elif len(name.decode("utf-8","ignore")) > 15:
            errtip.name = "请不要超过15个英文"
        else:
            site = zsite_new_site(name, current_user_id)
            return self.redirect(site.link)

        self.render(
            errtip=errtip,
            site=site,
            name=name,
            url=url
        )
