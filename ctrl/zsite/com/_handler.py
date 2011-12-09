#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from model.zsite_member import zsite_member_can_admin

from model.cid import CID_COM

class AdminBase(ZsiteBase):
    def prepare(self):
        super(AdminBase, self).prepare()
        zsite = self.zsite
        if not zsite.cid == CID_COM or not zsite_member_can_admin(self.zsite_id, self.current_user_id):
            self.redirect('/')

