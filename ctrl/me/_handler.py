# -*- coding: utf-8 -*-
from config import render
import model._db
from ctrl.zsite._handler import LoginBase


class Base(LoginBase):
    def prepare(self):
        super(Base, self).prepare()
        current_user = self.current_user_id
        path = self.request.path
        link = '%s%s'%(current_user.link, path)
        if current_user_id:
            self.redirect("/") 
