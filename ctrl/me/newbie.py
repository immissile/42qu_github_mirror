# -*- coding: utf-8 -*-
from ctrl._urlmap.me import urlmap

from _handler import LoginBase 
from model.zsite import Zsite
from zkit.errtip import Errtip
from model.zsite_show import SHOW_LIST
from model.user_auth import UserPassword, user_password_new
from model.user_info import user_info_new, UserInfo as _UserInfo


@urlmap('/i/guide')
class Career(CareerEdit):
    def post(self):
        self.save()
        self.redirect('/me/newbie/2')



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
        self.redirect('%s/feed'%current_user.link)

@urlmap('/i/guide')
class Newbie0(LoginBase):
    def get(self):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        current_user = self.current_user
        self.render(
            zsite_list=zsite_list,
            errtip=Errtip(),
            current_user=current_user
        )


    def post(self):
        name = self.get_argument('name', None)
        sex = self.get_argument('sex', '0')
        errtip = Errtip()
        current_user = self.current_user
        current_user_id = current_user.id

        info = _UserInfo.mc_get(current_user_id)
        if not (info and info.sex):
            if not(sex and int(sex) in (1, 2)):
                errtip.sex = '请选择性别'

        password = UserPassword.get(current_user_id)
        if not password:
            password = self.get_argument('password', None)
            if not password:
                errtip.password = '请输入密码'
            else:
                user_password_new(current_user_id, password)

        if name:
            current_user.name = name
            current_user.save()

        if not errtip:
            path = '/i/guide'
            user_info_new(current_user.id, sex=sex)
            return self.redirect(path)

        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        return self.render(
                   sex=sex,
                   name=name,
                   errtip=errtip,
                   zsite_list=zsite_list,
               )



@urlmap('/me/newbie/5')
class Newbie5(LoginBase):
    def get(self):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        current_user = self.current_user
        self.render(
            zsite_list=zsite_list,
            errtip=Errtip(),
            current_user=current_user
        )

