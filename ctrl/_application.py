#!/usr/bin/env python
#coding:utf-8

def main():
    import tornado.wsgi
    import _urlmap
    urlmap = tuple(_urlmap.URLMAP)
    application = tornado.wsgi.WSGIApplication(urlmap)
    return application

application = main()

