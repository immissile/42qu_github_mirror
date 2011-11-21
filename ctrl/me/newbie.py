# -*- coding: utf-8 -*-
from ctrl._urlmap.me import urlmap
from ctrl.me.i import UserInfoEdit, CareerEdit , PicEdit, LinkEdit
from _handler import LoginBase , XsrfGetBase
from model.zsite import Zsite
from zkit.errtip import Errtip
from model.zsite_show import SHOW_LIST

@urlmap('/me/newbie/1')
class Career(CareerEdit):
    def post(self):
        self.save()
        self.redirect('/me/newbie/2')


@urlmap('/me/newbie/2')
class Pic(PicEdit):
    def post(self):
        error_pic = self.save()
        if error_pic is None:
            if self.get_argument('pos', ''):
                self.redirect('/me/newbie/3')
        self.render(error_pic=error_pic, pos='')


@urlmap('/me/newbie/3')
class UserInfo(UserInfoEdit):
    def post(self):
        self.save()
        self.redirect('/me/newbie/4')


@urlmap('/me/newbie/4')
class Link(LinkEdit):
    def post(self):
        self.save()
        current_user = self.current_user
        self.redirect('%s/live'%current_user.link)

@urlmap('/me/newbie/0')
class Newbie0(LoginBase):
    def get(self):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        self.render(
            zsite_list=zsite_list,
            errtip=Errtip(),
        )

