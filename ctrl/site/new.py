# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from zkit.txt import cnenlen
from model.zsite import zsite_new_site, ZSITE_STATE_VERIFY, ZSITE_STATE_ACTIVE, ZSITE_STATE_APPLY
from model.zsite_url import url_valid, url_new
from model.zsite_link import OAUTH_LINK_DEFAULT
from model.oauth import OAUTH2NAME_DICT, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_QQ
from model.motto import motto as _motto
from model.txt import txt_get, txt_new


@urlmap('/new')
class SiteNew(LoginBase):
    def get(self):
        current_user = self.current_user
        if current_user.state < ZSITE_STATE_VERIFY:
            return self.finish('请认证')
        self.render(
            errtip=JsDict(),
        )

    def post(self):
        current_user_id = self.current_user_id
        current_user = self.current_user

        name = self.get_argument('name', None)
        url = self.get_argument('url', None)
        motto = self.get_argument('motto', None)
        txt = self.get_argument('txt', '')
        sitetype = self.get_argument('sitetype', None)

        errtip = Errtip()

        if not name:
            errtip.name = '请输入名称'
        elif cnenlen(name) > 18:
            errtip.name = '请不要超过九个汉字'
        elif len(name.decode("utf-8","ignore")) > 15:
            errtip.name = "请不要超过15个英文"

        url_err = url_valid(url)
        if url_err:
            errtip.url = url_err

        if sitetype not in ('1', '2'):
            sitetype = '1'
        if sitetype == '1':
            state = ZSITE_STATE_ACTIVE
        else:
            state = ZSITE_STATE_APPLY

        if errtip:
            zsite = None
        else:
            zsite = zsite_new_site(name, current_user_id, state)
            zsite_id = zsite.id
            url_new(zsite_id, url)
            if motto:
                _motto.set(zsite_id, motto)
            if txt:
                txt_new(zsite_id, txt)
            return self.redirect(zsite.link)

        self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            url=url,
            txt=txt,
        )
