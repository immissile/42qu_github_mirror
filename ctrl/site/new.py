# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from model.zsite import zsite_new, ZSITE_STATE_APPLY, ZSITE_STATE_VERIFY
from model.cid import CID_SITE


@urlmap('/new')
class SiteNew(LoginBase):
    def get(self):
        self.render(
            errtip=JsDict(),
        )

    def post(self):
        current_user_id = self.current_user_id
        current_user = self.current_user
        if current_user.state < ZSITE_STATE_VERIFY:
            return

        errtip = Errtip()
        name = self.get_argument('name', None)
        site = None
        if not name:
            errtip.name = '缺少名字'
        elif len(name) > 9:
            errtip.name = '最长9个字'
        else:
            site = zsite_new(name, CID_SITE, ZSITE_STATE_APPLY)
        self.render(
            errtip=errtip,
            site=site,
        )
