#!/usr/bin/env python
# -*- coding: utf-8 -*-


def domain_middleware(func):
    from config.zpage_host import SITE_DOMAIN
    from config.zpage_ctrl import PORT
    from model.zsite_link import zsite_by_domain
    from model._db import mc
    site = 'http://%s'%SITE_DOMAIN
    if PORT!=80:
        site = "%s:%s"%(site,PORT)

    def _(environ, start_response):
        mc.reset()
        host = environ['HTTP_HOST'].rsplit(":",1)[0]
        if host.startswith(SITE_DOMAIN):
            if len(host) == len(SITE_DOMAIN):
                return func(environ, start_response)
        else:
            zsite = zsite_by_domain(host)
            if zsite:
                return func(environ, start_response)
            else:
                start_response('301 Redirect', [
                    ('Location', site),
                ])
                return []
    return _
