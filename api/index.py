#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase
from _urlmap import urlmap
from model.oauth2 import oauth_client_new, oauth_client_web_new

from model.oauth2 import OauthClient, oauth_client_uri
from model.txt import txt_get


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap('/apply/(\d+)')
class Apply(LoginBase):
    def get(self, cid):
        self.render(cid = cid)

    def post(self, cid):
        current_user = self.current_user
        user_id = self.current_user_id
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        cid = self.get_argument('cid', '')
        site = self.get_argument('site', '')
        if cid:
            uri = self.get_argument('uri')
            oauth_client_web_new(user_id, name, txt, uri, site, cid)
        
        else:
            oauth_client_new(user_id, name, txt, site)
        return self.redirect('/')


@urlmap('/apply/edit/(\d+)')
class ApplyEdit(LoginBase):
    def get(self, id):
        client = OauthClient.get(id) 
        self.template = '/api/index/apply.htm'
        self.render(
            cid = client.cid,
            name = client.name,
            site = client.site,
            uri = oauth_client_uri.get(id),
            txt = txt_get(id),
            )

