# -*- coding: utf-8 -*-
from ctrl._urlmap.me import urlmap

from _handler import LoginBase , XsrfGetBase
from model.zsite import Zsite
from zkit.errtip import Errtip
from model.zsite_show import SHOW_LIST
from model.user_auth import user_password_verify, UserPassword, user_password_new
from model.user_info import user_info_new


@urlmap('/me/guide')
class Guide(LoginBase):
    def get(self, mail=''):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        self.render(
            mail=mail,
            sex=0,
            password='',
            errtip=Errtip(),
            zsite_list=zsite_list,
        )


