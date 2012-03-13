#!/usr/bin/env python
#coding:utf-8
import config
import config.dev

from server_ctrl import run
from zweb.server_cherry import WSGIServer

run.wsgi_server = WSGIServer

if __name__ == '__main__':
    print "\n%s\n"%config.SITE_HTTP

    from zkit.reloader.reload_server import auto_reload
    auto_reload(run)
    

