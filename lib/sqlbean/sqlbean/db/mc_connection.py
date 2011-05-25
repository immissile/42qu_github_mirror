import sys, os
import marshal
class SimpleCached:
    " cache obj in local process, wrapper for memcache "
    def __init__(self, mc):
        self.mc = mc

    def set_marshal(self, key, val, time=0, dumps=marshal.dumps):
        val = dumps(val)
        self.mc.set(key, val, time)

    def get_marshal(self, key, loads=marshal.loads):
        r = self.mc.get(key)
        if r is not None:
            r = loads(r)
        return r

    def get_multi_marshal(self, keys, loads=marshal.loads):
        rs = self.mc.get_multi(keys)
        rs = dict((k, loads(v)) for k, v in rs.iteritems())
        return rs

    def get_list_marshal(self, keys, loads=marshal.loads):
        rs = self.get_multi_marshal(keys, loads)
        return [rs.get(k) for k in keys]

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.mc, name)(*args, **kwargs)
        return func

    def reset(self):
        pass

class LocalCached:
    " cache obj in local process, wrapper for memcache "
    def __init__(self, mc):
        self.mc = mc
        self.reset()

    def reset(self):
        self.dataset = {}
        self.dataset_marshal = {}

    def start_log(self):
        from mypy.profile_middleware import CallLogger
        self.mc = CallLogger(self.mc)

    def stop_log(self):
        from mypy.profile_middleware import CallLogger
        if isinstance(self.mc, CallLogger):
            self.mc = self.mc.obj

    def get_log(self):
        from collections import defaultdict
        d = defaultdict(int)
        nd = defaultdict(lambda: [0, 0])
        for call, ncall, cost in self.mc.log:
            d[call] += 1
            x = nd[ncall]
            x[0] += 1
            x[1] += cost
        return "Memcache access (%s/%s calls):\n\n%s\nDetail:\n\n%s\n" % \
                        (len(d), sum(d.itervalues()),
                         ''.join("%s: %d times, %f seconds\n" % (
                                                ncall, times, cost)
                                 for ncall, (times, cost)
                                 in sorted(nd.iteritems())),
                         ''.join("%s: %d times\n" % (key, n)
                                 for key, n in sorted(d.iteritems())))


    def __repr__(self):
        return "Locally Cached " + str(self.mc)

    def set(self, key, val, time=0):
        self.dataset[key] = val
        self.mc.set(key, val, time)

    def set_marshal(self, key, val, time=0, dumps=marshal.dumps):
        self.dataset_marshal[key] = val
        val = dumps(val)
        self.mc.set(key, val, time)

    def get(self, key):
        r = self.dataset.get(key)
        if r is None:
            r = self.mc.get(key)
            if r is not None:
                self.dataset[key] = r
        return r

    def get_marshal(self, key, loads=marshal.loads):
        r = self.dataset_marshal.get(key)
        if r is None:
            r = self.get(key)
            if r is not None:
                r = loads(r)
                self.dataset_marshal[key] = r
        return r

    def get_multi(self, keys):
        rs = [(k, self.dataset.get(k)) for k in keys]
        r = dict((k, v) for k, v in rs if v is not None)
        rs = self.mc.get_multi([k for k, v in rs if v is None])
        r.update(rs)
        self.dataset.update(rs)
        return r

    def get_multi_marshal(self, keys, loads=marshal.loads):
        rs = [(k, self.dataset_marshal.get(k)) for k in keys]
        r = dict((k, v) for k, v in rs if v is not None)
        rs = self.mc.get_multi([k for k, v in rs if v is None])
        rs = dict((k, loads(v)) for k, v in rs.iteritems())
        r.update(rs)
        self.dataset_marshal.update(rs)
        return r

    def get_list_marshal(self, keys, loads=marshal.loads):
        rs = self.get_multi_marshal(keys, loads)
        return [rs.get(k) for k in keys]

    def get_list(self, keys):
        rs = self.get_multi(keys)
        return [rs.get(k) for k in keys]

    def append(self, key, val):
        self.dataset.pop(key, None)
        return self.mc.append(key, val)

    def prepend(self, key, val):
        self.dataset.pop(key, None)
        return self.mc.prepend(key, val)

    def delete(self, key):
        self.dataset.pop(key, None)
        return self.mc.delete(key)

    def decr(self, key, val=1):
        self.dataset.pop(key, None)
        return self.mc.decr(key, val)

    def incr(self, key, val=1):
        self.dataset.pop(key, None)
        return self.mc.incr(key, val)

    def __getattr__(self, name):
        def func(*args, **kwargs):
            return getattr(self.mc, name)(*args, **kwargs)
        return func


mc = None

def init_mc(memcached_addr=None, disable_local_cached=False):

    global mc

    if not memcached_addr:
        import lrucache
        class FakeMemcacheClient(object):
            def __init__(self):
                self.cache = lrucache.LRUCache(4096)

            def __getattr__(self, *args, **kwargs):
                def func(*args, **kwargs):
                    return None
                return func

            def append(self, key, val):
                return 0

            def prepend(self, key, val):
                return 0

            def set(self, key, val, time=0):
                self.cache[key] = val
                return 1

            def delete(self, key, time=0):
                if key in self.cache:
                    del self.cache[key]
                return 0

            def get(self, key):
                if key in self.cache:
                    return self.cache[key]
                return None

            def get_raw(self, key):
                return None

            def get_multi(self, keys):
                keys = tuple(keys)
                return dict(zip(keys, self.get_list(keys)))

            def get_list(self, keys):
                result = []
                for key in keys:
                    result.append(self.get(key))
                return result

            def incr(self, key, val=1):
                if key in self.cache:
                    self.cache[key] += val
                return 0

            def decr(self, key, val=1):
                if key in self.cache:
                    self.cache[key] -= val
                return 0

            def clear(self):
                pass

        mc = FakeMemcacheClient()
    else:
        import cmemcached
        kw = {}
        kw['comp_threshold'] = 4096
        #kw['dist'] = cmemcached.DIST_CONSISTENT_KETAMA
        mc = cmemcached.Client(memcached_addr, **kw)


        if disable_local_cached:
            mc = SimpleCached(mc)
        else:
            mc = LocalCached(mc)

    return mc
