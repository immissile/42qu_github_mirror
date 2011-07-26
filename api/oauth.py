#!/usr/bin/env python
#coding:utf-8
from  _handler import LoginBase, Base
from _urlmap import urlmap
from model.oauth2 import OauthClientUri, oauth_authorize_code_new, oauth_secret_verify, oauth_authorization_code_verify, oauth_refresh_token_new, oauth_access_token_new, oauth_authorize_code_rm
import urllib


@urlmap('/oauth/authorize')
class OauthAuthorize(LoginBase):
    def get(self):
        client_id = self.get_argument('client_id', '')
        response_type = self.get_argument('response_type', '')
        redirect_uri = self.get_argument('redirect_uri', '')
        if response_type == 'code':
            if client_id:
                if OauthClientUri.get(client_id) == redirect_uri:
                    self.render(client_id=client_id)
                else:
                    self.finish({'error':'redirect_uri error!'})
            else:
                self.finish({'error':'no client_id!'})
        else:
            self.finish({'error':'response_type error!'})

    def post(self):
        uri = self.get_argument('uri')
        url = uri+'?'+urllib.urlencode({'code':oauth_authorize_code_new()})
        self.redirect(url)




@urlmap('/oauth/token')
class OauthToken(Base):
    def get(self):
        client_id = self.get_argument('client_id', '')
        client_secret = self.get_argument('client_secret', '')
        redirect_uri = self.get_argument('redirect_uri', '')
        grant_type = self.get_argument('grant_type', '')
        code = self.get_argument('code', '')
        user_id = self.current_user_id

        if grant_type == 'authorization_code':
            if oauth_authorization_code_verify(code):
                authorization_id = oauth_authorization_code_verify(code)
                if oauth_secret_verify(client_id, client_secret):
                    id, access_token = oauth_access_token_new(client_id, user_id)
                    refresh_token = oauth_refresh_token_new(client_id, id)
                    oauth_authorize_code_rm(authorization_id)

                    url = redirect_uri+'?'+urllib.urlencode({
                        'access_token':access_token,
                        'refresh_token':refresh_token,
                        'expires_in': 87063,
                        'scope': 'basic',
                        'user_id':user_id
                    })
                    self.redirect(url)
                else:
                    self.finish({'error':'oauth secret verify error'})
            else:
                self.finish({'error':'oauth authorization code verify error'})
        else:
            self.finish({'error':'grant type error'})

