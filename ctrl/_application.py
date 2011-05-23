#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    import tornado.wsgi
    from zweb import _urlmap
    urlmap = tuple(_urlmap.URLMAP)
    from pprint import pprint
    pprint(urlmap)
    application = tornado.wsgi.WSGIApplication(
        urlmap,
        login_url = "/login",
        xsrf_cookies = True,
    )

    from zweb._middleware import default_middleware
    application = default_middleware(application)
    return application

application = main()
