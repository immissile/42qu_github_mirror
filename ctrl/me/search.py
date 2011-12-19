# -*- coding: utf-8 -*-
from ctrl._urlmap.me import urlmap

from _handler import LoginBase , XsrfGetBase
from model.zsite import Zsite
from zkit.errtip import Errtip
from model.zsite_show import SHOW_LIST
from model.user_auth import user_password_verify, UserPassword, user_password_new
from model.user_info import user_info_new


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

