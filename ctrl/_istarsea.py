# -*- coding: utf-8 -*-
import _url_istarsea
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers
from config import SITE_URL

application = tornado.wsgi.WSGIApplication(
    login_url='/auth/login' ,
    xsrf_cookies=True,
)

RE_SITE_DOMAIN = SITE_DOMAIN.replace('.', r"\.")


import _urlmap_istarsea.istarsea
import _urlmap_istarsea.i

application.add_handlers(
    '.*',
    handlers(
        _urlmap_istarsea.istarsea,
        _urlmap_istarsea.i
    )
)

