#coding:utf-8

from mmhash import get_hash


# USEAGE :
# 
#class Shorturl(Model):
#    by_url_hash = by_hash("url")
#    
#    def save(self):
#        url = self.url
#        save_hash(self,"url")
#        super(Shorturl,self).save()


def by_hash(name):
    hk = name+'_hash'
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
        setattr(self, name+'_hash', h)

