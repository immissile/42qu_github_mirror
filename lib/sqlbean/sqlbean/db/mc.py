import sys, os
import marshal
from decorator import decorator
import inspect
from array import array
from struct import pack
from mc_connection import mc

def _mc_get_multi(self, args_list):
    if not isinstance(args_list, (list, tuple, dict, set)):
        args_list = tuple(args_list)
    if args_list:
        result = self.get_list(args_list)
        return dict(zip(args_list, result))
    return {}

def _mc_decorator(self, key, expire=0):
    if type(key) is str:
        _key = key
        key = lambda x:_key.format(**x)

    def _func(func):
        arg_names, varargs, varkw, defaults = inspect.getargspec(func)

        if varargs or varkw:
            raise Exception("do not support varargs")

        defaults = defaults or {}
        if defaults:
            args = dict(zip(arg_names[-len(defaults):], defaults))
        else:
            args = {}


        def _(f, *a, **kw):
            aa = args.copy()
            aa.update(zip(arg_names, a))
            aa.update(kw)
            mc_key = key(aa)

            #print mc_key
            r = self.get(mc_key)
            if r is None:
                r = f(*a, **kw)
                self.set(mc_key, r, expire)
            return r

        return decorator(_, func)
    return _func

def _mc_delete(self, *args):
    key = self.key_pattern%args
    return mc.delete(key)

class McCacheM(object):
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern

    def get(self, *args):
        key = self.key_pattern%args
        return mc.get_marshal(key)

    def set(self, key, value, expire=0):
        return mc.set_marshal(self.key_pattern%key, value, expire)

    def get_list(self, args_list):
        key_pattern = self.key_pattern
        key_list = [key_pattern%i for i in args_list]
        result = mc.get_list_marshal(key_list)
        return result

    get_multi = _mc_get_multi
    __call__ = _mc_decorator
    delete = _mc_delete

class McCache(object):
    """
    def test_mc_cache():
        mc_xxx = McCache("XXxxx:%s")

        @mc_xxx(lambda x:x['id'])
        def xxx(id):
            return id*3

        print  xxx("123")
        
        @mc_xxx("{id}")
        def xxx(id):
            return id*3

        print  xxx("467")
        print "MC GET" 
        print mc_xxx.get("123")
        print mc_xxx.get_multi(["123","467"])
        mc_xxx.delete("123")
    """
    def __init__(self, key_pattern):
        self.key_pattern = key_pattern

    def get(self, *args):
        key = self.key_pattern%args
        return mc.get(key)

    def set(self, key, value, expire=0):
        return mc.set(self.key_pattern%key, value, expire)

    def get_list(self, args_list):
        key_pattern = self.key_pattern
        key_list = [key_pattern%i for i in args_list]
        result = mc.get_list(key_list)
        return result

    def decr(self, *args):
        key = self.key_pattern%args
        return mc.decr(key)

    def incr(self, *args):
        key = self.key_pattern%args
        return mc.incr(key)

    __call__ = _mc_decorator
    get_multi = _mc_get_multi
    delete = _mc_delete


class McCacheA(object):
    def __init__(self, key_pattern, type='L'):
        self.key_pattern = key_pattern
        self.type = type

    def get(self, *args):
        key = self.key_pattern%args
        result = mc.get(key)
        if result is not None:
            return array(self.type, result)

    def set(self, key, value, expire=0):
        key = self.key_pattern%key
        if type(value) is not array:
            value = pack(self.type*len(value), *value)
        else:
            value = value.tostring()
        return mc.set(key, value, expire)

    def get_list(self, args_list):
        if args_list:
            key_pattern = self.key_pattern
            key_list = [key_pattern%i for i in args_list]
            result = []
            for i in mc.get_list(key_list):
                if i is None:
                    result.append(i)
                else:
                    result.append(array(self.type).fromstring(i))
            return result
        else:
            return []

    __call__ = _mc_decorator
    get_multi = _mc_get_multi
    delete = _mc_delete


class McLimitA(object):
    McCls = McCacheA
    def __init__(self, key_pattern, limit):
        self.mc = self.McCls(key_pattern)
        self.limit = limit
        self.key_pattern = key_pattern

    def __call__(self, key, expire=0):
        if type(key) is str:
            _key = key
            key = lambda x:_key.format(**x)

        def _func(func):
            arg_names, varargs, varkw, defaults = inspect.getargspec(func)

            if varargs or varkw:
                raise Exception("do not support varargs")

            defaults = defaults or {}
            if defaults:
                args = dict(zip(arg_names[-len(defaults):], defaults))
            else:
                args = {}


            def _(f, *a, **kw):
                aa = args.copy()
                aa.update(zip(arg_names, a))
                aa.update(kw)
                mc_key = key(aa)
                offset = aa.get('offset', 0)
                limit = aa.get('limit')
                if limit is None or offset+limit > self.limit:
                    return func(*a, **kw)
                smc = self.mc
                r = smc.get(mc_key)
                #print  mc_key,r
                if r is None:
                    aa['offset'] = 0
                    aa['limit'] = self.limit
                    r = f(**aa)
                    smc.set(mc_key, r, expire)
                return r[offset:limit+offset]
            return decorator(_, func)
        return _func


    def delete(self, *args):
        return self.mc.delete(*args)


class McLimit(McLimitA):
    McCls = McCache

class McLimitM(McLimitA):
    McCls = McCacheM



