#!/usr/bin/env python
#coding:utf-8
from _handler import Base, LoginBase, XsrfGetBase
from _urlmap import urlmap
from model.oauth2 import oauth_client_new, oauth_client_web_new

from model.oauth2 import OauthClient, oauth_client_uri, oauth_client_edit, oauth_client_web_edit

from model.txt import txt_get


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()


@urlmap('/apply/(\d+)')
class Apply(LoginBase):
    def get(self, cid):
        cid = int(cid)
        self.render(cid=cid)

    def post(self, cid):
        cid = int(cid)
        user_id = self.current_user_id
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        site = self.get_argument('site', '')
        if name:
            if cid:
                uri = self.get_argument('uri', '')
                oauth_client_web_new(user_id, name, txt, uri, site, cid)
            else:
                oauth_client_new(user_id, name, txt, site, cid)
        return self.redirect('/')


@urlmap('/apply/edit/(\d+)')
class ApplyEdit(LoginBase):
    template = '/api/index/apply.htm'

    def get(self, oauth_client_id):
        client = OauthClient.get(oauth_client_id)
        if client and client.can_admin(self.current_user_id):
            self.render(
                cid=client.cid,
                name=client.name,
                site=client.site,
                uri=oauth_client_uri.get(oauth_client_id),
                txt=txt_get(oauth_client_id),
                oauth_client_id=oauth_client_id,
            )
        else:
            return self.redirect('/')

    def post(self, oauth_client_id):
        client = OauthClient.get(oauth_client_id)
        if client and client.can_admin(self.current_user_id):
            name = self.get_argument('name', '')
            txt = self.get_argument('txt', '')
            site = self.get_argument('site', '')
            if client.cid:
                uri = self.get_argument('uri', '')
                oauth_client_web_edit(oauth_client_id, name, txt, site, uri, )
            else:
                oauth_client_edit(oauth_client_id, name, txt, site)
        return self.redirect('/')

@urlmap('/apply/rm/(\d+)')
class ApplyRm(XsrfGetBase):
    def get(self, oauth_client_id):
        client = OauthClient.get(oauth_client_id)
        if client and client.can_admin(self.current_user_id):
            client.rm()
        return self.redirect('/')
