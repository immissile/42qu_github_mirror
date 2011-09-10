# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from zkit.txt import cnenlen
from model.zsite import zsite_new_site, ZSITE_STATE_VERIFY, ZSITE_STATE_ACTIVE, ZSITE_STATE_APPLY
from model.zsite_url import url_valid, url_new
from model.zsite_link import SITE_LINK_DEFAULT, SITE_LINK_NAME, SITE_LINK_DICT, link_list_save, link_id_name_by_zsite_id, link_id_cid, link_by_id
from model.motto import motto as _motto
from model.txt import txt_get, txt_new
from urlparse import parse_qs, urlparse
from ctrl.me.i import linkify

DEFAULT_LINK_CID = tuple((i, j, '') for i, j in SITE_LINK_NAME)

@urlmap('/new')
class SiteNew(LoginBase):
    def get(self):
        current_user = self.current_user
        if current_user.state < ZSITE_STATE_VERIFY:
            return self.finish('请认证')
        self.render(
            errtip=JsDict(),
            link_cid=DEFAULT_LINK_CID,
            link_list=[],
        )

    def post(self):
        current_user_id = self.current_user_id
        current_user = self.current_user

        name = self.get_argument('name', '')
        url = self.get_argument('url', '')
        motto = self.get_argument('motto', '')
        txt = self.get_argument('txt', '')
        sitetype = self.get_argument('sitetype', '')

        arguments = parse_qs(self.request.body, True)
        link_cid = []
        link_kv = []
        for cid, link in zip(arguments.get('cid'), arguments.get('link')):
            cid = int(cid)
            name = SITE_LINK_DICT[cid]
            link_cid.append((cid, name, linkify(link, cid)))

        for id, key, value in zip(
            arguments.get('id'),
            arguments.get('key'),
            arguments.get('value')
        ):
            id = int(id)
            link = linkify(value)

            link_kv.append((id, key.strip() or urlparse(link).netloc, link))

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

            link_list_save(zsite_id, link_cid, link_kv)

            return self.redirect(zsite.link)

        self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            url=url,
            txt=txt,
            link_cid=link_cid,
            link_list=link_kv,
        )
