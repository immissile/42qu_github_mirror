#!/usr/bin/env python
# -*- coding: utf-8 -*-

def attrcache(f):
    name = f.__name__
    @property
    def _attrcache(self):
        if name in self.__dict__:
            return self.__dict__[name]
        result = f(self)
        self.__dict__[name] = result
        return result
    return _attrcache


class AttrCache(object):
    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        elif self.name in inst.__dict__:
            return inst.__dict__[self.name]
        else:
            result = self.method(inst)
            inst.__dict__[self.name] = result
            return result

    def __delete__(self, inst):
        del inst.__dict__[self.name]


class ReadOnlyAttrCache(AttrCache):
    def __set__(self, inst, value):
        raise AttributeError('This property is read-only')
