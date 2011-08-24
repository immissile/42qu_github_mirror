from model.oauth import OAUTH_GOOGLE, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_WWW163,  OAUTH_SOHU, OAUTH_QQ, OAUTH_RENREN, oauth_save_douban, oauth_save_www163, oauth_save_qq, oauth_save_sohu, oauth_save_twitter, oauth_save_sina

from _handler import LoginBase
from mixin import DoubanMixin, GoogleMixin, Www163Mixin, QqMixin, TwitterMixin, SinaMixin
import tornado.web
from _urlmap import urlmap
from config import SITE_DOMAIN

BACK_URL = 'http://%%s.%s/i/bind'%SITE_DOMAIN
#+SITE_DOMAIN

@urlmap('/oauth/%s'%OAUTH_DOUBAN)
class DoubanOauthHandler(LoginBase, DoubanMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )

    def _on_auth(self, user):
        zsite = self.current_user

        back = BACK_URL%zsite.id

        if user:
            access_token = user.get('access_token')

            if access_token:
                oauth_save_douban(
                    zsite.id,
                    access_token['key'],
                    access_token['secret'],
                    user['name'],
                    user['uid'],
                )
        return self.redirect(back)


@urlmap('/oauth/%s'%OAUTH_GOOGLE)
class GoogleOauthHandler(LoginBase, GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('openid.mode', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return


@urlmap('/oauth/%s'%OAUTH_SINA)
class SinaOauthHandler(LoginBase, SinaMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )

    def _on_auth(self, user):
        man = self.current_user
        back = BACK_URL%man.id
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_sina(
                        man.id,
                        access_token['key'],
                        access_token['secret'],
                        user['name'],
                        user['domain'] or user['id']
                    )

            return self.redirect(back)



@urlmap('/oauth/%s'%OAUTH_WWW163)
class Www163OauthHandler(LoginBase, Www163Mixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )
    def _on_auth(self, user):
        man = self.current_user
        back = BACK_URL%man.id
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_www163(
                        man.id,
                        access_token['key'],
                        access_token['secret'],
                        user['name'],
                        user['screen_name'],
                            )
                return self.redirect(back)




@urlmap('/oauth/%s'%OAUTH_QQ)
class QqOauthHandler(LoginBase, QqMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
            self.callback_url()
                )


    def _on_auth(self, user):
        zsite = self.current_user
        back = BACK_URL%zsite.id
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_qq(
                            zsite.id,
                            access_token['key'],
                            access_token['secret'],
                            access_token['name'],
                            access_token['name']                        )
                return self.redirect(back)

#@urlmap('/oauth/%s'%OAUTH_SOHU)
#class SohuOauthHandler(LoginBase, SohuMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument('oauth_token',None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#        self.authorize_redirect(
#                self.callback_url()
#                )
#    
#    def _on_auth(self, user):
#        man = self.current_user
#        back = '/'
#        if user:
#            access_token = user.get('access_token')
#            if access_token:
#                oauth_save_sohu(
#                        man.id,
#                        access_token['key'],
#                        access_token['secret'],
#                        user['name'],
#                        user['screen_name']
#                        )
#                return self.redirect(back)
#                


@urlmap('/oauth/%s'%OAUTH_TWITTER)
class TwitterOauthHandler(LoginBase, TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(
                self.callback_url()
                )

    def _on_auth(self, user):
        man = self.current_user
        back = BACK_URL%man.id
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_twitter(
                        man.id,
                        access_token['key'],
                        access_token['secret'],
                        user['name'],
                        user['username'],
                        )
                return self.redirect(back)

