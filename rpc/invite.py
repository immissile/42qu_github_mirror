#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from _urlmap import urlmap
from config import SITE_URL
from model.invite_email import CID_GOOGLE, CID_MSN, new_invite_email, get_email_by_cid, msn_friend_get
import tornado.web
from tornado.auth import GoogleMixin
import thread


@urlmap('/invite/msn')
class MsnAsync(LoginBase):
    @tornado.web.asynchronous
    def get(self):
        email = self.get_argument('email',None)
        passwd = self.get_argument('passwd',None)
        if email and passwd:
            res = msn_friend_get(email,passwd)
        new_invite_email(self.current_user_id,email,CID_MSN,res)
        self.finish({'frd_list':get_email_by_cid(self.current_user_id,CID_MSN)})

class _GoogleMixin(GoogleMixin):
    _OAUTH_VERSION = "1.0"

    def _oauth_get_user(self,access_token,callback):
        self.access_token = access_token
        super(self,GoogleMixin)._oauth_get_user(access_token,callback)

@urlmap('/invite/google')
class GoogleAsync(LoginBase,_GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return

        self.authorize_redirect("https://www.google.com/m8/feeds/",'http://rpc.yup.xxx/invite/google' ,ax_attrs=["name", "email","language","username"])

    def _on_auth(self, userj):
        print userj,'!!!!!!!!!'
        
        email = None

        if userj:
            email = userj.get("email")

        if not email:
            self.redirect("/invite/google")
            return

        user = self.current_user
        access_token = userj['access_token']
        key = access_token['key']
        secret = access_token['secret']
        user_id = str(user.id)

        if user.email == email:#TODO 支持多个email
            pass
            #oauth_save_google(user_id, key, secret)

        thread.start_new_thread(
            async_load_friend,
            ( user_id, key, secret)
        )

    
    def async_load_friend( user_id, key, secret, callback ):
        result = load_friend(key, secret)
        self.finish({'hg':result})








if __name__ == "__main__":
    print tornado.auth.__file__









#
#
#
#
#
#@urlmap('/')
#class GoogleHandler(LoginBase,GoogleMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument("openid.mode", None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#
#        self.authorize_redirect("http://www.google.com/m8/feeds/", ax_attrs=["name", "email"])
#
#    def _on_auth(self, userj):
#        email = None
#
#        if userj:
#            email = userj.get("email")
#
#        if not email:
#            self.redirect("/me/load_friend")
#            return
#
#        user = self.get_user()
#        if user is None:
#            self.redirect("/auth/login")
#            return
#
#        access_token = userj['access_token']
#        key = access_token['key']
#        secret = access_token['secret']
#        user_id = str(user.id)
#
#        if user.email == email:#TODO 支持多个email
#            oauth_save_google(user_id, key, secret)
#
#        thread.start_new_thread(
#            async_load_friend,
#            ( user_id, key, secret, self.async_callback(self._load_friend))
#        )
#
#    def _load_friend(self, save_id):
#        self.redirect("/me/load_friend/loaded/%s"%save_id)
#        self.finish()
