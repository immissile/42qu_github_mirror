#!/usr/bin/env python
#coding:utf-8


def main():
    import tornado.ioloop
    import tornado.web
    from zweb import _urlmap

    urlmap = tuple(_urlmap.URLMAP)

    application = tornado.web.Application(
        urlmap
    )

    application = default_middleware(application)
    return application

application = main()


