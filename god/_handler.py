#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.privilege import has_privilege_by_user_id_path
from zweb._handler.main import LoginBase

class Base(LoginBase):
    def prepare(self):
        current_user_id = self.current_user_id
        if has_privilege_by_user_id_path(current_user_id, self.request.path):
            super(Base, self).prepare()
        else:
            self.redirect('/')

    def post(self, *arg, **kwds):
        return self.get(*arg, **kwds)
