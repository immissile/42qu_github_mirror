#!/usr/bin/env python
#coding:utf-8

def main():
    import tornado.wsgi
    from zweb import _urlmap
    urlmap = tuple(_urlmap.URLMAP)
    application = tornado.wsgi.WSGIApplication(
        urlmap,
        login_url="/login",
    )

    from zweb._middleware import default_middleware
    application = default_middleware(application)
    return application

application = main()


