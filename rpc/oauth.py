from model.oauth import OAUTH_GOOGLE, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_WWW163, OAUTH_SOHU, OAUTH_QQ, OAUTH_RENREN,OAUTH_RENREN, oauth_save_douban, oauth_save_www163, oauth_save_qq, oauth_save_sohu, oauth_save_twitter, oauth_save_sina, oauth_save_renren, OAUTH_KAIXIN, oauth_save_kaixin
from model.zsite_url import url_or_id
from _handler import LoginBase
from mixin import DoubanMixin, GoogleMixin, Www163Mixin, QqMixin, TwitterMixin, SinaMixin, SohuMixin, RenrenMixin, KaixinMixin
import tornado.web
from _urlmap import urlmap
from config import SITE_DOMAIN
import urlparse

BACK_URL = 'http://%s/i/bind'%SITE_DOMAIN


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
        print BACK_URL
        return self.redirect(BACK_URL)


@urlmap('/oauth/%s'%OAUTH_GOOGLE)
class GoogleOauthHandler(LoginBase, GoogleMixin):
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
        if user:
            access_token = user.get('access_token')
            if access_token:
                print access_token
        return self.redirect(BACK_URL)
                    

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

            return self.redirect(BACK_URL)

@urlmap('/oauth/%s'%OAUTH_KAIXIN)
class KaixinOauthHandler(LoginBase, KaixinMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code',None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        callback = urlparse.urljoin(self.request.full_url(),self.callback_url())
        token = self._oauth_consumer_token()
        print callback
        self.authorize_redirect(
            callback,
            token['key'],
            token['secret'],
            {'response_type':'code',
                'scope':'create_records'}
        )
    def _on_auth(self,user):
        uid = self.current_user_id
        if user:
            access_token = user.get('access_token')
            if access_token:
                print user
                oauth_save_kaixin(
                        uid,
                        access_token,
                        user.get('refresh_token'),
                        user.get('name'),
                        user.get('uid')
                        )
            return self.redirect(BACK_URL)

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
                return self.redirect(BACK_URL)




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
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_qq(
                            zsite.id,
                            access_token['key'],
                            access_token['secret'],
                            access_token['name'],
                            access_token['name']                        )
                return self.redirect(BACK_URL)

@urlmap('/oauth/%s'%OAUTH_SOHU)
class SohuOauthHandler(LoginBase, SohuMixin):
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
        back = '/'
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_sohu(
                        man.id,
                        access_token['key'],
                        access_token['secret'],
                        user['name'],
                        user['screen_name']
                        )
                return self.redirect(back)

@urlmap('/oauth/%s'%OAUTH_RENREN)
class RenrenOauthHandler(LoginBase, RenrenMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code',None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        callback = urlparse.urljoin(self.request.full_url(),self.callback_url())
        token = self._oauth_consumer_token()
        self.authorize_redirect(
            callback,
            token['client_id'],
            token['client_secret'],
            {'response_type':'code',
                'scope':'status_update publish_share'}
        )
    def _on_auth(self,user):
        uid = self.current_user_id
        if user:
            access_token = user.get('access_token')
            if access_token:
                oauth_save_renren(
                        uid,
                        access_token,
                        user.get('refresh_token'),
                        user.get('user').get('name'),
                        user.get('user').get('id')
                        )
            return self.redirect(BACK_URL)

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
                return self.redirect(BACK_URL)

