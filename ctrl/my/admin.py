# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.my import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from zkit.txt import cnenlen
from model.zsite import zsite_name_edit

PAGE_LIMIT = 20

@urlmap('/edit')
class SiteEdit(LoginBase):
    def get(self):
        self.render(
            errtip=JsDict(),
        )

    def post(self):
        zsite_id = self.zsite_id
        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        txt = self.get_argument('txt', '')

        errtip = Errtip()

        if not name:
            errtip.name = '请输入名称'
        elif cnenlen(name) > 18:
            errtip.name = '请不要超过九个汉字'
        elif len(name.decode("utf-8","ignore")) > 15:
            errtip.name = "请不要超过15个英文"
        else:
            zsite_name_edit(zsite_id, name)

        if motto:
            _motto.set(zsite_id, motto)
        if txt:
            txt_new(zsite_id, txt)

        self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            txt=txt,
        )
