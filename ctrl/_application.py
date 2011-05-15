#!/usr/bin/env python
#coding:utf-8

def main():
    import tornado.wsgi
    import _urlmap
    urlmap = tuple(_urlmap.URLMAP)
    application = tornado.wsgi.WSGIApplication(
        urlmap,
        login_url = "/login",
        xsrf_cookies = True,
    )

    from _middleware import domain_middleware
    application = domain_middleware(application)
    return application

application = main()

