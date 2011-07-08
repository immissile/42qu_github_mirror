# -*- coding: utf-8 -*-
from ctrl.me.i import UserInfoEdit, CareerEdit , PicEdit

@urlmap('/auth/newbie/1')
class Career(CareerEdit):
    def post(self):
        self.save()
        self.redirect('/auth/newbie/2')


@urlmap('/auth/newbie/2')
class Pic(PicEdit):
    def post(self):
        error_pic = self.save()
        if error_pic is None:
            if self.get_argument('pos', ''):
                self.redirect('/auth/newbie/3')
        self.render(error_pic=error_pic, pos='')

@urlmap('/auth/newbie/3')
class UserInfo(UserInfoEdit):
    def post(self):
        self.save()
        current_user = self.current_user
        self.redirect("%s/live"%current_user.link)

