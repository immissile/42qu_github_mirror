#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.main import urlmap
from config import SITE_URL
from model.zsite_url import zsite_by_domain
from model.cid import CID_SITE
from model.po import po_word_new


@urlmap('/share')
class Share(LoginBase):
    def get(self,success=None):
        name = self.get_argument('name',None)
        href = self.get_argument('href',None)
        zsite = self.current_user
        if success:
            self.render(success=success,zsite=zsite)
        self.render(name=name,href=href,zsite=zsite)


    def post(self):
        name =  self.get_argument('name',None)
        href =  self.get_argument('href',None)
        current_user_id = self.current_user_id
        txt = self.get_argument('word', None)
        if not href:
            name = ''.join([name,'[[',href,']]'])
        txt = name+txt
        if txt:
            host = self.request.host
            zsite = zsite_by_domain(host)
            if zsite and zsite.cid == CID_SITE:
                zsite_id = zsite.id
            else:
                zsite_id = 0

            m = po_word_new(current_user_id, txt, zsite_id=zsite_id)

        self.get('ok')
