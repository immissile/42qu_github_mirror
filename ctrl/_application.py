# -*- coding: utf-8 -*-
import _url
import tornado.wsgi
from config import SITE_DOMAIN
from zweb.urlmap import handlers

application = tornado.wsgi.WSGIApplication(
    login_url='/login',
    xsrf_cookies=True,
)


import main._urlmap
application.add_handlers(
    SITE_DOMAIN.replace(".",r"\."),
    handlers(main._urlmap)
)

import me._urlmap
import zsite._urlmap
import j._urlmap
application.add_handlers(
    ".*",
    handlers(zsite._urlmap, j._urlmap, me._urlmap)
)
