#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.main import urlmap

@urlmap('/po/\w+')
class Po(LoginBase):
    def get(self):
        current_user = self.current_user
        self.redirect(current_user.link + self.request.path)
