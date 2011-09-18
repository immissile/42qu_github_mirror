# -*- coding: utf-8 -*-
from _handler import ZsiteBase, _login_redirect

class SiteBase(ZsiteBase):
    def prepare(self):
        super(SiteBase, self).prepare()
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




