#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.user_mail import user_by_mail
from model.ico import ico96

@urlmap('/user/info/mail')
class Index(_handler.ApiBase):
    def get(self):
        mail = self.get_argument('mail',0)
        user = user_by_mail(mail)
        data = {}
        if user:
            user_id = user.id
            data['user_id'] = user_id
            data['name'] = user.name
            data['ico96'] = ico96.get(user_id) 
        self.finish(data)


@urlmap('/user/auth/login')
def Login(_handler.ApiSignBase):
    def get(self):
        user_id = self.get_argument(user_id,0)
        auth = self.get_argument(auth)
        
        



