# -*- coding: utf-8 -*-
import _url
import main._urlmap
import zsite._urlmap
import j._urlmap
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers

application = tornado.wsgi.WSGIApplication(
    login_url='/login',
    xsrf_cookies=True,
)

application.add_handlers(
    SITE_DOMAIN.replace(".",r"\."),
    handlers(main._urlmap, j._urlmap)
)

application.add_handlers(
    ".*",
    handlers(zsite._urlmap, j._urlmap)
)
