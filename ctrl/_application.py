# -*- coding: utf-8 -*-
import _url
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers
from config import SITE_URL
from _urlmap import auth, hero, j, main, me, meet, my, site, zsite

application = tornado.wsgi.WSGIApplication(
    login_url='/auth/login' ,
    xsrf_cookies=True,
)

RE_SITE_DOMAIN = SITE_DOMAIN.replace('.', r"\.")

application.add_handlers(
    'hero\.%s'%RE_SITE_DOMAIN,
    handlers(hero, auth)
)

application.add_handlers(
    'meet\.%s'%RE_SITE_DOMAIN,
    handlers(meet, auth)
)

application.add_handlers(
    'site\.%s'%RE_SITE_DOMAIN,
    handlers(site, auth)
)

application.add_handlers(
    RE_SITE_DOMAIN,
    handlers(main, auth)
)

application.add_handlers(
    '.*',
    handlers(auth, me, zsite, j, my)
)
