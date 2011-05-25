#coding:utf-8
from sqlbean.db.mc_connection import mc
class McTotal(object):
    def __init__(self, get_count, mc_key, timeout=36000):
        self.mc_key = mc_key
        self.get_count = get_count
        self.timeout = timeout

    def __call__(self, key):
        mk = self.mc_key%key
        count = mc.get(mk)
        if count is None:
            count = self.get_count(key) or 0
            mc.set(mk, count, self.timeout)
        return count

    def get_multi(self, keys):
        mc_key = self.mc_key
        mc_key_list = dict([(key, mc_key%key) for key in keys])
        result = mc.get_multi(mc_key_list.itervalues())
        r = {}
        for k, mck in mc_key_list.iteritems():
            v = result.get(mck)
            if v is None:
                v = self.get_count(k) or 0
                mc.set(mck, v)
            r[k] = v
        return r

    def bind(self, xxx_list, property, key="id"):
        d = []
        e = []
        for i in xxx_list:
            k = getattr(i, key)
            if k:
                d.append(k)
                e.append((k, i))
            else:
                i.__dict__[property] = None

        r = self.get_multi(set(d))
        for k, v in e:
            v.__dict__[property] = r.get(k)

    def delete(self, key):
        mk = self.mc_key%key
        mc.delete(mk)

    def get_list(self, keys):
        r = self.get_multi(keys)

        return [
            r.get(i, 0) for i in keys
        ]


    def incr(self, key):
        mk = self.mc_key%key
        if mc.get(mk) is not None:
            mc.incr(mk)

    def decr(self, key):
        mk = self.mc_key%key
        if mc.get(mk) is not None:
            mc.decr(mk)


