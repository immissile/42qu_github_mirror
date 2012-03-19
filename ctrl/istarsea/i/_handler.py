# -*- coding: utf-8 -*-
from config import render
import model._db
from ctrl.zsite._handler import LoginBase as _LoginBase

class LoginBase(_LoginBase):
    def prepare(self):
        super(LoginBase, self).prepare()
        if not self._finished and self.zsite_id != self.current_user_id:
            current_user_link = self.current_user.link
            path = self.request.path
            link = '%s%s'%(current_user_link, path)
            return self.redirect(link)
