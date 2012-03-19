# -*- coding: utf-8 -*-
from ctrl._urlmap.me import urlmap
from config import SITE_URL
from _handler import LoginBase 
from model.zsite import Zsite
from zkit.errtip import Errtip
from model.zsite_show import SHOW_LIST
from model.user_auth import user_password_verify, UserPassword
from ctrl.me.i import PicEdit

@urlmap('/i/guide')
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


@urlmap('/i/guide/pic')
class Pic(PicEdit):
    def post(self):
        error_pic = self.save()
        if error_pic is None:
            if self.get_argument('pos', ''):
                self.redirect(SITE_URL)
        self.render(error_pic=error_pic, pos='')



