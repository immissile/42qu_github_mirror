#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from zkit.zitertools import lineiter
from array import array
from po_tag import tag_alias_by_id_query

REDIS_ZSET_CID = '%s`'
REDIS_ID2NAME = 'ACId2Name:%s'
REDIS_CACHE = 'ACCache:%s'


__metaclass__ = type
EXPIRE = 86400


class AutoComplete:
    #别名可以自动补全

    def __init__(self, name):
        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
        self.CACHE = '%s%%s'%(REDIS_CACHE%name)

    def _set_cache(self, key, id_list):
        key = self.CACHE%key
        result = array('I')
        result.fromlist(list(map(int, id_list)))
        redis.setex(
            key, result.tostring(), EXPIRE
        )

    def _get_cache(self, key):
        key = self.CACHE%key
        r = redis.get(key)
        if r is not None:
            t = array('I')
            t.fromstring(r)
        else:
            t = None
        return t

    def append_alias(self, name, id, rank=1):
        from zkit.fanjian import ftoj
        name = ftoj(name.decode('utf-8', 'ignore'))
        self._append(name, id, rank)

    def append(self, name, id , rank=1):
        from zkit.fanjian import ftoj
        name = ftoj(name.decode('utf-8', 'ignore'))
        ID2NAME = self.ID2NAME

        if rank is None:
            rank = 0

        value = redis.hget(ID2NAME, id)
        if value:
            #TODO 如果rank不一样, 需要进行修改
            #TODO 如果name不一样, 需要删除然后重新索引
            return
        
        tag_name = name.replace('`', "'").strip()
        redis.hset(ID2NAME, id, '%s`%s'%(tag_name, rank))
        self._append(tag_name, id, rank)

    def _key(self, name):
        from zkit.pinyin import pinyin_list_by_str

        tag_name = name.lower().replace('/', ' ').strip()

        if not tag_name:
            return

        ZSET_CID = self.ZSET_CID

        for sub_tag in tag_name.split(' '):
            for pos in xrange(1, len(sub_tag)+1):
                key = sub_tag[:pos]
                yield ZSET_CID%key

            pylist = pinyin_list_by_str(sub_tag)
            for py in pylist:
                yield ZSET_CID%py

            for pos in xrange(2, len(pylist)+1):
                yield ZSET_CID%"".join(pylist[:pos])

    def pop_alias(self, name, id):
        for i in self._key(name):
            redis.zrem(i, id)    

    def _append(self, name, id, rank=1):
        for i in self._key(name):
            redis.zadd(i, id, rank) 

    def id_list_by_str(self, query, limit=7):
        name_list = query.strip().lower().replace('`', "'").split()
        if not name_list:
            return []

        name_list.sort()

        name_key = '`'.join(name_list)
        id_list = self._get_cache(name_key)

        #id_list = None #TODO REMOVE
        ZSET_CID = self.ZSET_CID

        if id_list is None:
            mkey = ZSET_CID%name_key

            if not redis.exists(mkey):
                p = redis.pipeline()
                p.zinterstore(mkey, map(ZSET_CID.__mod__, name_list), 'MAX')
                p.expire(mkey, EXPIRE)
                p.execute()

            id_list = redis.zrevrange(mkey, 0, limit)
            self._set_cache(name_key, id_list)

        return id_list


    def id_rank_name_list_by_str(self, query):
        result = []
        id_list = self.id_list_by_str(query)
        if id_list:
            for id, name_rank in zip(id_list, redis.hmget(self.ID2NAME, id_list)):
                name, rank = name_rank.rsplit('`', 1)
                if query not in name:
                    alias = tag_alias_by_id_query(id,query) or 0 
                else:
                    alias = 0
                result.append(
                    (id, rank, name,alias)
                )
        return result

autocomplete_tag = AutoComplete('tag')

if __name__ == '__main__':
    pass
    #autocomplete_tag = AutoComplete('tag')
    #autocomplete_tag.append('Facebook/F8', 76514)
    #autocomplete_tag.append('flask', 76515)
    #for i in autocomplete_tag.id_name_list_by_key("f"):
    #    print i
    #print "=+++"

    from zkit.pprint import pprint
    pprint(autocomplete_tag.id_rank_name_list_by_str('baidu'))
    #print autocomplete_tag.id_rank_name_list_by_str('f')
    print redis.keys('tag`baidu')
    #from timeit import timeit
    #def f():
    #    autocomplete_tag.id_name_list_by_name_list('t')

    #print timeit(f,number=10000)/10000
