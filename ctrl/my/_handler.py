# -*- coding: utf-8 -*-
from config import render
import model._db
from ctrl.zsite._handler import LoginBase as _LoginBase, XsrfGetBase
from model.zsite_admin import admin_id_list_by_zsite_id

class LoginBase(_LoginBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        if not self._finished and self.current_user_id not in admin_id_list_by_zsite_id(self.zsite_id):
            zsite = self.zsite
            return self.redirect(zsite.link)
