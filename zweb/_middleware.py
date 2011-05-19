#!/usr/bin/env python
# -*- coding: utf-8 -*-

def default_middleware(func):
    from model._db import mc
    def _(environ, start_response):
        mc.reset()
        return func(environ, start_response)
    return _



