# -*- coding: utf-8 -*-
import _url
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers
from config import SITE_URL

application = tornado.wsgi.WSGIApplication(
    login_url='/auth/login' ,
    xsrf_cookies=True,
)

RE_SITE_DOMAIN = SITE_DOMAIN.replace('.', r"\.")


import _urlmap.hero
import _urlmap.auth
application.add_handlers(
    'hero\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.hero, _urlmap.auth)
)

import _urlmap.meet
import _urlmap.auth
application.add_handlers(
    'meet\.%s'%RE_SITE_DOMAIN,
    handlers(_urlmap.meet, _urlmap.auth)
)


import _urlmap.main
import _urlmap.auth
application.add_handlers(
    RE_SITE_DOMAIN,
    handlers(_urlmap.main, _urlmap.auth)
)

import _urlmap.auth
import _urlmap.me
import _urlmap.zsite
import _urlmap.j

application.add_handlers(
    '.*',
    handlers(_urlmap.auth, _urlmap.me, _urlmap.zsite, _urlmap.j)
)
