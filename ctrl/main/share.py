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
    
    def get(self):
        name, href = self._argument()
        self.render(name=name,href=href)

    def _argument(self):
        name = self.get_argument('name',None)
        href = self.get_argument('href',None)
        if href:
            try:
                href = href.decode("utf-8")
            except:
                href = href.decode("gb18030")
            if not href.startswith("http://") or not http.startswith("https://"):
                href = "http://"+href
            
        if name:
            try:
                name = name.decode("utf-8")
            except:
                name = name.decode("gb18030")
        return name, href

    def post(self):
        name, href = self._argument()
        current_user_id = self.current_user_id
        txt = self.get_argument('word', None)
        if href:
            if name:
                name = ''.join([name,'[[',href,']]'])
                txt = name+txt
            else:
                txt = "[["+href+"]]"+txt
        elif name:
            txt = name+" "+txt

        if txt:
            host = self.request.host
            zsite = zsite_by_domain(host)
            if zsite and zsite.cid == CID_SITE:
                zsite_id = zsite.id
            else:
                zsite_id = 0

            m = po_word_new(current_user_id, txt, zsite_id=zsite_id)

        self.render(success=True)

