#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import SITE_DOMAIN, SITE_URL, ADMINISTRATORS
from zweb._handler.main import LoginBase

class Base(LoginBase):
    def prepare(self):
        current_user_id = self.current_user_id
        if current_user_id in ADMINISTRATORS:
            print "!!!!!"
        else:
            print current_user_id, self.request.path

        super(Base, self).prepare()

    def post(self, *arg, **kwds):
        return self.get(*arg, **kwds)
