#!/usr/bin/env python
#coding:utf-8

def main():
    import tornado.wsgi
    import _url
    _url_map = tuple(_url.MAP)
    application = tornado.wsgi.WSGIApplication(_url_map)
    return application

application = main()

