from model.oauth import OAUTH_GOOGLE, OAUTH_DOUBAN, OAUTH_SINA, OAUTH_TWITTER, OAUTH_WWW163, OAUTH_BUZZ, OAUTH_SOHU, OAUTH_QQ, OAUTH_RENREN, oauth_save_douban
from _handler import LoginBase
from mixin import DoubanMixin
import tornado.web
from _urlmap import urlmap




@urlmap('/oauth/%s'%OAUTH_DOUBAN)
class DoubanOauthHandler(LoginBase, DoubanMixin):
    @tornado.web.asynchronous
    def get(self):
        zsite = self.get_current_user()
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
                self.callback_url()
                )
    
    def _on_auth(self,user):
        zsite = self.get_current_user()

        back = "/"

        if zsite:
            access_token = zsite.get('access_token')

            if access_token:
                oauth_save_douban(
                    zsite.id,
                    access_token['key'],
                    access_token['secret'],
                    zsite['name'],
                    zsite['uid'],
                )
            #back = "%s/%s"%(back, OAUTH_DOUBAN)
        return self.redirect(back)


