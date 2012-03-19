# -*- coding: utf-8 -*-
from _handler import ZsiteBase, _login_redirect
from model.cid import CID_SITE, CID_COM
from model.zsite_site import site_can_admin

class SiteBase(ZsiteBase):
    def prepare(self):
        super(SiteBase, self).prepare()
        zsite = self.zsite
        current_user_id = self.current_user_id

        if zsite.cid not in (CID_SITE, CID_COM):
            return self.redirect('/')



class LoginBase(SiteBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        _login_redirect(self)


class XsrfGetBase(LoginBase):
    def prepare(self):
        super(XsrfGetBase, self).prepare()
        self.check_xsrf_cookie()


class AdminBase(SiteBase):
    def prepare(self):
        super(AdminBase, self).prepare()
        _login_redirect(self)

        zsite = self.zsite
        zsite_id = self.zsite_id
        current_user_id = self.current_user_id

        if not site_can_admin(zsite_id, current_user_id):
            return self.redirect('/')
