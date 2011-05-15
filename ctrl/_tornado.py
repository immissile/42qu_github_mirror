#!/usr/bin/env python
#coding:utf-8


from tornado import web
from config.zpage_host import SITE_DOMAIN_SUFFIX

_set_cookie = web.RequestHandler.set_cookie

def set_cookie(
    self, name, value, domain=SITE_DOMAIN_SUFFIX, expires=None, path="/",
    expires_days=None, **kwargs
):
    _set_cookie(
        self,
        name, value, domain, expires,
        path, expires_days, **kwargs
    )


web.RequestHandler.set_cookie = set_cookie
