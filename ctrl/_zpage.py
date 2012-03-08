# -*- coding: utf-8 -*-
import _url_zpage
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers
from config import SITE_URL

application = tornado.wsgi.WSGIApplication(
    login_url='/auth/login' ,
    xsrf_cookies=True,
)

RE_SITE_DOMAIN = SITE_DOMAIN.replace('.', r"\.")

import _urlmap.auth
import _urlmap.j

import _urlmap.hero
application.add_handlers(
    'hero\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.hero, _urlmap.auth, _urlmap.j)
)

import _urlmap.meet
application.add_handlers(
    'meet\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.meet, _urlmap.auth, _urlmap.j)
)

import _urlmap.site
application.add_handlers(
    'site\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.site, _urlmap.auth, _urlmap.j)
)

import _urlmap.tag
application.add_handlers(
    'tag\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.tag, _urlmap.auth, _urlmap.j)
)

import _urlmap.com
application.add_handlers(
    'com\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.com, _urlmap.auth, _urlmap.j)
)

import _urlmap.star
application.add_handlers(
    'star\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.star, _urlmap.auth, _urlmap.j)
)

import _urlmap.main
application.add_handlers(
    RE_SITE_DOMAIN,
    handlers(_urlmap.main, _urlmap.auth, _urlmap.j)
)

import _urlmap.auth
import _urlmap.me
import _urlmap.zsite
import _urlmap.j

application.add_handlers(
    '.*',
    handlers(_urlmap.auth, _urlmap.me, _urlmap.zsite, _urlmap.j)
)

