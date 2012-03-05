from model.oauth import OAUTH_GOOGLE, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_WWW163, OAUTH_SOHU, OAUTH_QQ, OAUTH_RENREN, OAUTH_RENREN, oauth_save_douban, oauth_save_www163, oauth_save_qq, oauth_save_sohu, oauth_save_twitter, oauth_save_sina, oauth_save_renren, OAUTH_KAIXIN, oauth_save_kaixin, OAUTH_FANFOU, oauth_save_fanfou
from model.zsite_url import url_or_id
from _handler import LoginBase, Base as _Base
from mixin import DoubanMixin, GoogleMixin, Www163Mixin, QqMixin, TwitterMixin, SinaMixin, SohuMixin, RenrenMixin, KaixinMixin, FanfouMixin
import tornado.web
from _urlmap import urlmap
from config import SITE_DOMAIN
import urlparse
from urllib import quote
from model.user_session import user_session, user_session_rm
from model.user_mail import mail_by_user_id
from model.oauth import zsite_id_by_token_key_login
from model.zsite import Zsite

BACK_URL = '//%s/i/bind'%SITE_DOMAIN

LOGIN_REDIRECT = '%s/feed'

class Base(_Base):
    def prepare(self):
        super(Base, self).prepare()
        self.oauth_key = 0

    def _login(self, user_id):
        session = user_session(user_id)
        mail = mail_by_user_id(user_id)

        self.set_cookie('S', session)
        self.set_cookie('E', mail)

        current_user = Zsite.mc_get(user_id)

        redirect = LOGIN_REDIRECT%current_user.link
        self.redirect(redirect)


    def _on_auth(self, user):
        if user:
            current_user_id = self.current_user_id
            key = self._on_auth_key(user)
            if not current_user_id:
                user_id = zsite_id_by_token_key_login(self.cid, key)
                if user_id:
                    return self._login(user_id)

            id = self._on_auth_save(user)
            if not current_user_id and id:
                return self.redirect('http://%s/auth/bind/%s?key=%s'%(SITE_DOMAIN, id, quote(key)))

            return self.redirect(BACK_URL)

    def _on_auth_key(self, user):
        access_token = user.get('access_token')
        key = access_token['key']
        return key

@urlmap('/oauth/(\d+)/login')
class OauthLogin(Base):
    def get(self, id):
        if self.current_user:
            url = LOGIN_REDIRECT%self.current_user.link
        else:
            url = '/oauth/%s'%id
        return self.redirect(url)

@urlmap('/oauth/%s'%OAUTH_DOUBAN)
class DoubanOauthHandler(Base, DoubanMixin):
    cid = OAUTH_DOUBAN

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
            self.callback_url()
        )


    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_douban(
            self.current_user_id,
            access_token['key'],
            access_token['secret'],
            user['name'],
            user['uid'],
        )

@urlmap('/oauth/%s'%OAUTH_FANFOU)
class FanfouOauthHandler(Base, FanfouMixin):
    cid = OAUTH_FANFOU

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )

    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_fanfou(
            self.current_user_id,
            access_token['key'],
            access_token['secret'],
            user['name'],
            user['id']
        )





@urlmap('/oauth/%s'%OAUTH_SINA)
class SinaOauthHandler(Base, SinaMixin):
    cid = OAUTH_SINA

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )

    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_sina(
                self.current_user_id,
                access_token['key'],
                access_token['secret'],
                user['name'],
                user['domain'] or user['id']
            )


@urlmap('/oauth/%s'%OAUTH_KAIXIN)
class KaixinOauthHandler(Base, KaixinMixin):
    cid = OAUTH_KAIXIN
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        callback = urlparse.urljoin(self.request.full_url(), self.callback_url())
        token = self._oauth_consumer_token()
        self.authorize_redirect(
            callback,
            token['key'],
            token['secret'],
            {'response_type':'code',
                'scope':'create_records'}
        )

    def _on_auth_key(self, user):
        return user.get('access_token')

    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_kaixin(
            self.current_user_id,
            access_token,
            user.get('refresh_token'),
            user.get('name'),
            user.get('uid')
        )

@urlmap('/oauth/%s'%OAUTH_RENREN)
class RenrenOauthHandler(Base, RenrenMixin):
    cid = OAUTH_RENREN
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        callback = urlparse.urljoin(self.request.full_url(), self.callback_url())
        token = self._oauth_consumer_token()
        self.authorize_redirect(
            callback,
            token['client_id'],
            token['client_secret'],
            {'response_type':'code',
                'scope':'status_update publish_share'}
        )

    def _on_auth_key(self, user):
        return user.get('access_token')

    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_renren(
                    self.current_user_id,
                    access_token,
                    user.get('refresh_token'),
                    user.get('user').get('name'),
                    user.get('user').get('id')
                )

@urlmap('/oauth/%s'%OAUTH_WWW163)
class Www163OauthHandler(Base, Www163Mixin):
    cid = OAUTH_WWW163
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
        )

    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_www163(
                self.current_user_id,
                access_token['key'],
                access_token['secret'],
                user['name'],
                user['screen_name'],
            )




@urlmap('/oauth/%s'%OAUTH_QQ)
class QqOauthHandler(Base, QqMixin):
    cid = OAUTH_QQ
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
            self.callback_url()
        )


    def _on_auth_save(self, user):
        access_token = user.get('access_token')
        return oauth_save_qq(
            self.current_user_id,
            access_token['key'],
            access_token['secret'],
            access_token['name'],
            access_token['name']
        )



##@urlmap('/oauth/%s'%OAUTH_TWITTER)
##class TwitterOauthHandler(Base, TwitterMixin):
##    @tornado.web.asynchronous
##    def get(self):
##        if self.get_argument('oauth_token', None):
##            self.get_authenticated_user(self.async_callback(self._on_auth))
##            return
##        self.authenticate_redirect(
##                self.callback_url()
##                )
##
##    def _on_auth(self, user):
##        man = self.current_user
##        if user:
##            access_token = user.get('access_token')
##            if access_token:
##                oauth_save_twitter(
##                        man.id,
##                        access_token['key'],
##                        access_token['secret'],
##                        user['name'],
##                        user['username'],
##                        )
##                return self.redirect(BACK_URL)
##
##
##
##@urlmap('/oauth/%s'%OAUTH_GOOGLE)
##class GoogleOauthHandler(Base, GoogleMixin):
##    @tornado.web.asynchronous
##    def get(self):
##        if self.get_argument('oauth_token', None):
##            self.get_authenticated_user(self.async_callback(self._on_auth))
##            return
##        self.authorize_redirect(
##                self.callback_url()
##                )
##
##    def _on_auth(self, user):
##        man = self.current_user
##        if user:
##            access_token = user.get('access_token')
##            if access_token:
##                print access_token
##        return self.redirect(BACK_URL)

#@urlmap('/oauth/%s'%OAUTH_TWITTER)
#class TwitterOauthHandler(Base, TwitterMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument("oauth_token", None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#        self.authorize_redirect()
#
#    def _on_auth(self, user):
#        if user:
#            access_token = user.get('access_token')
#            if access_token:
#                oauth_save_fanfou(
#                        self.current_user_id,
#                        access_token['key'],
#                        access_token['secret'],
#                        user['name'],
#                        user['id']
#                    )
#            return self.redirect(BACK_URL)

#@urlmap('/oauth/%s'%OAUTH_SOHU)
#class SohuOauthHandler(Base, SohuMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument('oauth_token', None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#        self.authorize_redirect(
#                self.callback_url()
#                )
#
#    def _on_auth(self,user):
#        man = self.current_user
#        if user:
#            access_token = user.get('access_token')
#            if access_token:
#                print user
#                #oauth_save_fanfou(
#                #        man.id,
#                #        access_token['key'],
#                #        access_token['secret'],
#                #        user['name'],
#                #        user['id']
#                #    )
#            return self.redirect(BACK_URL)
#@urlmap('/oauth/%s'%OAUTH_SOHU)
#class SohuOauthHandler(Base, SohuMixin):
#    @tornado.web.asynchronous
#    def get(self):
#        if self.get_argument('oauth_token', None):
#            self.get_authenticated_user(self.async_callback(self._on_auth))
#            return
#        self.authorize_redirect(
#                self.callback_url()
#                )
#
#    def _on_auth(self, user):
#        back = '/'
#        if user:
#            access_token = user.get('access_token')
#            if access_token:
#                oauth_save_sohu(
#                        self.current_user_id,
#                        access_token['key'],
#                        access_token['secret'],
#                        user['name'],
#                        user['screen_name']
#                        )
#                return self.redirect(back)
