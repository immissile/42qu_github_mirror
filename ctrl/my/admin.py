# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.my import urlmap
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from zkit.errtip import Errtip
from zkit.txt import cnenlen
from model.zsite import zsite_name_edit
from model.zsite_link import SITE_LINK_DEFAULT, SITE_LINK_NAME, SITE_LINK_DICT, link_list_save, link_id_name_by_zsite_id, link_id_cid, link_by_id
from model.motto import motto as _motto
from model.txt import txt_get, txt_new
from urlparse import parse_qs, urlparse
from ctrl.me.i import linkify

PAGE_LIMIT = 20

@urlmap('/edit')
class SiteEdit(LoginBase):
    def get(self):
        zsite_id = self.zsite_id
        id_name = link_id_name_by_zsite_id(zsite_id)
        id_cid = dict(link_id_cid(zsite_id))

        link_list = []
        link_cid = []
        exist_cid = set()

        for id, name in id_name:
            link = link_by_id(id)
            if id in id_cid:
                cid = id_cid[id]
                link_cid.append((cid, name , link))
                exist_cid.add(cid)
            else:
                link_list.append((id, name, link))

        for cid in (set(SITE_LINK_DEFAULT) - exist_cid):
            link_cid.append((cid, SITE_LINK_DICT[cid], ''))

        return self.render(
            link_list=link_list,
            link_cid=link_cid,
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

        link_list_save(zsite_id, link_cid, link_kv)

        self.get()
