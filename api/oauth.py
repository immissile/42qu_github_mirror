#!/usr/bin/env python
#coding:utf-8
import _handler
from _urlmap import urlmap


@urlmap('/oauth/authorize')
class OauthAuthorize(_handler.LoginBase):
    def get(self):
        arg = self.request
        self.render(arg=arg)

        def post(self):
            current_user = self.current_user
            arg = self.get_argument('arg')

            if arg:
                client_id = arg['client_id']
                redirect_uri = arg['redirect_uri']
                response_type = arg['response_type']
            pass


@urlmap('/oauth/token')
class OauthToken(_handler.Base):
    def get(self):
        arg = self.request
        #if arg:
        pass 


