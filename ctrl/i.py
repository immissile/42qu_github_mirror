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

@urlmap("/i")
class Setting(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        files = self.request.files
        current_user_id = self.current_user_id
        error_img = None
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                ico_new(current_user_id, pic)
            else:
                error_img = "图片格式有误"
        _motto = self.get_argument('motto', None)
        if _motto:
            motto.set(current_user_id, _motto)
        self.render(
           error_img=error_img
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
        self.render(
            pid_now=c.pid_now or 0,
            pid_home=c.pid_home or 0,
            name=c.name or current_user.name,
            phone=c.phone,
            mail=c.mail,
            address=c.address,
        )

    def post(self):
        current_user = self.current_user
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now', '1')
        name = self.get_argument('name', '')
        phone = self.get_argument('phone', '')
        mail = self.get_argument('mail', '')
        address = self.get_argument('address', '')
        pid_now = int(pid_now)
        if pid and name and phone and mail and address:
            c = namecard_new(current_user_id, pid_now, name, phone, mail, address)
        self.render(
            pid_now=pid_now,
            name=name or current_user.name,
            phone=phone,
            mail=mail,
            address=address,
        )

