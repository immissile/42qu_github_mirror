#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from zweb._urlmap import urlmap
from zkit.pic import picopen
from zkit.jsdict import JsDict
from model.motto import motto
from model.namecard import namecard_get, namecard_new
from model.ico import ico_new
from model.zsite_link import url_by_id, url_new, url_valid
from model.user_mail import mail_by_user_id

def _upload_pic(files, current_user_id):
    error_pic = None
    if 'pic' in files:
        pic = files['pic'][0]['body']
        pic = picopen(pic)
        if pic:
            ico_new(current_user_id, pic)
            error_pic = False
        else:
            error_pic = "图片格式有误"
    return error_pic



@urlmap("/i/pic")
class Pic(_handler.LoginBase):
    def get(self):
        pos = ""
        self.render(pos=pos)

    def post(self):
        current_user_id = self.current_user_id
        files = self.request.files
        pos = self.get_argument('pos', '')
        error_pic = _upload_pic(files, current_user_id)
        self.render(error_pic=error_pic, pos=pos)


@urlmap("/i")
class Index(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id
        current_user = self.current_user

        _name = self.get_argument('name', None)
        if _name:
            current_user.name = _name
            current_user.save()

        _motto = self.get_argument('motto', None)
        if _motto:
            motto.set(current_user_id, _motto)

        error_pic = _upload_pic(files, current_user_id)
        if error_pic is False:
            return self.redirect("/i/pic")

        self.render(
           error_pic=error_pic
        )

@urlmap('/i/url')
class Url(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        user_id = self.current_user_id
        url = self.get_argument('url', None)
        if url:
            if url_by_id(user_id):
                error_url = '个性域名设置后不能修改'
            else:
                error_url = url_valid(url)
            if error_url is None:
                url_new(user_id, url)
        else:
            error_url = '个性域名不能为空'
        self.render(
            error_url=error_url
        )

@urlmap('/i/namecard')
class Namecard(_handler.LoginBase):
    def get(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        c = namecard_get(current_user_id) or JsDict()
        pid_now = c.pid_now
        pid_home = c.pid_home
        birthday = str(c.birthday).zfill(8)
        self.render(
            pid_now=pid_now or 0,
            pid_home=pid_home or 0,
            name=c.name or current_user.name,
            phone=c.phone,
            mail=c.mail or mail_by_user_id(current_user_id),
            address=c.address,
            birthday=birthday
        )

    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now', '1')
        pid_home = self.get_argument('pid_home', '1')
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')
        birthday = self.get_argument('birthday', '00000000')

        pid_now = int(pid_now)
        pid_home = int(pid_home)
        birthday = int(birthday)

        if pid_now or pid_home or name or phone or mail or address or birthday:
            c = namecard_new(
                current_user_id, birthday,
                pid_home, pid_now, name, phone, mail, address
            )

        self.render(
            pid_now=pid_now,
            pid_home=pid_home,
            name=name or current_user.name,
            phone=phone,
            mail=mail,
            address=address,
            birthday=birthday
        )

