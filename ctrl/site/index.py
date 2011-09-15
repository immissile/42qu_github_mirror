# -*- coding: utf-8 -*-

from _handler import Base
from ctrl._urlmap.site import urlmap
from zkit.jsdict import JsDict
from urlparse import parse_qs, urlparse
from zkit.page import page_limit_offset
from model.oauth import linkify
from model.zsite_link import SITE_LINK_NAME,SITE_LINK_ZSITE_DICT
from model.zsite_link import OAUTH2NAME_DICT, link_list_save, link_id_name_by_zsite_id, link_id_cid, link_by_id, OAUTH_LINK_DEFAULT
from zkit.errtip import Errtip



PAGE_LIMIT = 25


@urlmap('/')
class Index(Base):
    def get(self):
        return self.render()

@urlmap('/new')
class New(Base):
    def get(self):
        link_cid = []
        for cid, name in SITE_LINK_NAME:
            link_cid.append(
                (
                    cid,
                    name, 
                    ''
                )
            )
        return self.render(
            errtip=JsDict(),
            link_cid=link_cid,
            link_list=[]
        )

    def post(self):
        arguments = parse_qs(self.request.body, True)
        link_cid = []
        link_kv = []
        errtip = Errtip()

        name = self.get_argument('name',None)
        motto = self.get_argument('motto', None)
        url = self.get_argument('url', None)
        txt = self.get_argument('txt', None)
        sitetype = int(self.get_argument('sitetype'))



        for cid, link in zip(arguments.get('cid'), arguments.get('link')):
            cid = int(cid)
            name = SITE_LINK_ZSITE_DICT[cid]
            link_cid.append(
                (cid, name, linkify(link, cid))
            )

        for id, key, value in zip(
            arguments.get('id'),
            arguments.get('key'),
            arguments.get('value')
        ):
            id = int(id)
            link = linkify(value)

            link_kv.append(
                (id, key.strip() or urlparse(link).netloc, link)
            )

#        link_list_save(zsite_id, link_cid, link_kv)

        return self.render(
            errtip=errtip,
            link_cid=link_cid,
            link_list=link_kv,
            name=name,
            motto=motto,
            url=url,
            sitetype=sitetype,
            txt=txt,
        )



