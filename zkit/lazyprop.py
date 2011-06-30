#!/usr/bin/env python
# -*- coding: utf-8 -*-

def attrcache(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _attrcache(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _attrcache
