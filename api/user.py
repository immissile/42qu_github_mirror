#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.user_mail import user_by_mail, mail_by_user_id
from model.user_auth import user_password_sha256, sha256
from model.api_client import api_session_new
from model.api_user import json_info

@urlmap('/user/info/mail')
class InfoMail(_handler.ApiBase):
    def get(self):
        mail = self.get_argument('mail')
        user = user_by_mail(mail)
        data = json_info(user.id) 
        self.finish(data)


@urlmap('/user/auth/login')
class Login(_handler.ApiSignBase):
    def get(self):
        user_id = self.get_argument('user_id')
        auth = self.get_argument('token')
        client_id = self.get_argument('client_id')
        password = user_password_sha256(user_id)
        if not password:
            return self.finish('{}')

        if auth != sha256(mail_by_user_id(user_id)+password).hexdigest():
            return self.finish('{}')

        self.finish({
            'S':api_session_new(client_id, user_id)
        })

@urlmap('/user/info/id')
class InfoId(_handler.ApiBase):
    def get(self):
        user_id = self.get_argument('user_id')
        data = json_info(user_id) 
        self.finish(data)







