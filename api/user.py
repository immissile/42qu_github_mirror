#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.user_mail import user_by_mail, mail_by_user_id
from model.zsite import Zsite
from model.motto import motto
from model.zsite_link import url_by_id
from model.txt import txt_get
from model.ico import ico96, ico
from model.namecard import namecard_get
from model.user_auth import user_password_sha256, sha256
from model.api_client import api_session_new
from model.follow import follow_count_by_to_id, follow_count_by_from_id
@urlmap('/user/info/mail')
class InfoMail(_handler.ApiBase):
    def get(self):
        mail = self.get_argument('mail')
        user = user_by_mail(mail)
        data = {}
        if user:
            user_id = user.id
            data['user_id'] = user_id
            data['name'] = user.name
            data['ico'] = ico96.get(user_id)
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
        user = Zsite.mc_get(user_id)
        txt = txt_get(user_id)
        data = {}
        namecard = namecard_get(user_id)
        if user:
            data['user_id'] = user_id
            data['self_intro'] = txt
            data['name'] = user.name
            data['ico'] = ico96.get(user_id)
            data['moto'] = motto.get(user_id)
            data['user_link'] = url_by_id(user_id)
            data['sex'] = namecard.sex
            data['marry'] = namecard.marry
            data['place_home'] = namecard.pid_home
            data['place_now'] = namecard.pid_now
            data['follower_num'] = follow_count_by_to_id(user_id)
            data['following_num'] = follow_count_by_from_id(user_id)
            data['verify_state'] = user.state
            data['pic'] = ico.get(user_id)
        self.finish(data)







