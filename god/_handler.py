#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.privilege import has_privilege_by_user_id_path
from zweb._handler.main import LoginBase

class Base(LoginBase):
    def prepare(self):
        super(Base, self).prepare()
        current_user_id = self.current_user_id
        if self._finished:
            return
        if not has_privilege_by_user_id_path(current_user_id, self.request.path):
            self.redirect('/')

    def post(self, *arg, **kwds):
        return self.get(*arg, **kwds)
