#!/usr/bin/env python
# -*- coding: utf-8 -*-



def domain_middleware(func):
    from config.zpage_host import SITE_HOST
    from config.zpage_ctrl import PORT
    from model._db import mc
    site = 'http://%s'%SITE_HOST
    if PORT!=80:
        site = "%s:%s"%(site,PORT)

    def _(environ, start_response):
        mc.reset()
        host = environ['HTTP_HOST'].rsplit(":",1)[0]
        if host.startswith(SITE_HOST):
            if len(host) == len(SITE_HOST):
                return func(environ, start_response)
        else:
            pid = 0
            if pid:
                return func(environ, start_response)
            else:
                start_response('301 Redirect', [
                    ('Location', site),
                ])
                return []
    return _
