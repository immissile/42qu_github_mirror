# -*- coding: utf-8 -*-
from _handler import ZsiteBase, _login_redirect
from model.cid import CID_SITE
from model.zsite_site import ZSITE_STATE_SITE_SECRET, site_can_view

class SiteBase(ZsiteBase):
    def prepare(self):
        super(SiteBase, self).prepare()
        zsite = self.zsite
        current_user_id = self.current_user_id

        if zsite.cid != CID_SITE:
            return self.redirect("/")



class LoginBase(SiteBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)


class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()




