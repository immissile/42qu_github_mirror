#!/usr/bin/env python
#coding:utf-8


from server_istarsea import run
from zweb.server_cherry import WSGIServer

run.wsgi_server = WSGIServer



if __name__ == '__main__':
    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
