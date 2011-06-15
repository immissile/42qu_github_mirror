#!/usr/bin/env python
# -*- coding: utf-8 -*-
import main._urlmap
import zsite._urlmap
import j._urlmap
import tornado.wsgi
from config import SITE_DOMAIN

application = tornado.wsgi.WSGIApplication(
    login_url='/login',
    xsrf_cookies=True,
)

#from zweb._urlmap import URLMAP
#tuple(URLMAP)
#        application.add_handlers(r"www\.myhost\.com", [
#            (r"/article/([0-9]+)", ArticleHandler),
#        ])

application.add_handlers(
    SITE_DOMAIN.replace(".",r"\."), 
    handlers(main._urlmap, j._urlmap)
)

application.add_handlers(
    "",
    handlers(main._urlmap, j._urlmap)
)
