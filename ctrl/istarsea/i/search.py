# -*- coding: utf-8 -*-
from ctrl._urlmap_istarsea.i import urlmap

from _handler import LoginBase 
from model.user_auth import user_password_verify, UserPassword


@urlmap('/me/search')
class Search(LoginBase):
    def get(self):
        self.render()

    def post(self):
        self.render()

@urlmap('/me/search/next')
class SearchNext(LoginBase):
    def get(self):
        self.render()

