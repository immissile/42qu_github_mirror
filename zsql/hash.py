#coding:utf-8

from mmhash import get_hash


# USEAGE :
# 
# class RssSource(Model):
#     _by_source_hash = by_hash("source")
# 
#     @classmethod
#     def by_source_hash(cls, source):
#         if source.startswith("http://www.google.com/reader"):
#             source = "https"+source[4:]
#         return cls._by_source_hash(source)
# 
#     def save(self):
#         source = self.source
#         save_hash(self, "source")
#         super(RssSource, self).save()


def by_hash(name):
    hk = name+"_hash"
    @classmethod
    def _by_hash(cls, key):
        for i in cls.where(
            **{
                hk:get_hash(key)
            }
        ):
            if getattr(i, name) == key:
                return i
    return _by_hash


def save_hash(self, name):
    if self._new_record or (name in self._changed):
        h = get_hash( getattr(self, name) )
        setattr(self, name+"_hash", h)

