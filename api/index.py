#!/usr/bin/env python
#coding:utf-8


from zweb._handler.me import Base, LoginBase
from _urlmap import urlmap
from model.api_client import api_client_new

@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap('/apply')
class Apply(LoginBase):
    def get(self):
        self.render()

    def post(self):
        current_user = self.current_user
        user_id = self.current_user_id
        name = self.get_argument('name', current_user.name)
        txt = self.get_argument('txt', '')
        api_client_new(user_id, name, txt)
        return self.redirect('/')

