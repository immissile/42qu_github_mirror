#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import authenticated
import _handler
from zweb._urlmap import urlmap
from zkit.pic import picopen
from model.pic import ico_new
from model.zsite_link import url_by_id, url_new, url_valid
from model.namecard import get_namecard, namecard_new

@urlmap("/i")
class Setting(_handler.LoginBase):
    def get(self):
        self.render()

    def post(self):
        files = self.request.files
        current_user = self.current_user
        error_img = None
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                ico_new(current_user.id, pic)
            else:
                error_img = "图片格式有误"
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
        namecard = get_namecard(self.current_user_id)
        self.render()

    def post(self):
        pid = self.get_argument('pid', None)
        name = self.get_argument('name', None)
        phone = self.get_argument('phone', None)
        mail = self.get_argument('mail', None)
        address = self.get_argument('address', None)
