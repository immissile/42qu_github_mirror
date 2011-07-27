#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase
from _urlmap import urlmap
from model.oauth2 import oauth_client_new, oauth_client_web_new



@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap('/apply')
class Apply(LoginBase):
    def get(self):
        cid = self.get_argument('cid',0)
        self.render(cid = cid)

    def post(self):
        current_user = self.current_user
        user_id = self.current_user_id
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        cid = self.get_argument('cid')
        if cid:
            uri = self.get_argument('uri')
            oauth_client_web_new(user_id,name,txt,uri)
        
        else:
            oauth_client_new(user_id, name, txt)
        return self.redirect('/')
