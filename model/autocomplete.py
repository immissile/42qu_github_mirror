#!/usr/bin/env python
# -`- coding: utf-8 -`-

from array import array

from _db import redis
from zkit.zitertools import lineiter
from zkit.algorithm.unique import unique

REDIS_ZSET_CID = '%s`'
REDIS_ID2NAME = 'ACId2Name:%s'
REDIS_NAME2ID = 'ACName2Id:%s'
REDIS_CACHE = 'ACCache:%s'


__metaclass__ = type
EXPIRE = 86400


class AutoComplete:
    #别名可以自动补全

    def __init__(self, name, alias_by_id_query):
        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
        self.NAME2ID = '%s'%(REDIS_NAME2ID%name)
        self.CACHE = '%s%%s'%(REDIS_CACHE%name)
        self.alias_by_id_query = alias_by_id_query

    def _set_cache(self, key, id_list):
        key = self.CACHE%key
        result = array('I')
        result.fromlist(id_list)
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
        self._name2id_set(name,id )

    def append(self, name, id , rank=1):
        from zkit.fanjian import ftoj
        name = ftoj(name.decode('utf-8', 'ignore'))
        ID2NAME = self.ID2NAME

        if rank is None:
            rank = 0

        value = redis.hget(ID2NAME, id)

        _append = False
        if value:
            value_name, value_rank = value.rsplit('`', 1)
            if value_name != name:
                ZSET_CID = self.ZSET_CID
                p = redis.pipeline()
                for i in self._key(value_name):
                    p.delete(CACHE%i)
                    p.zrem(ZSET_CID%i, id)
                p.execute()
                _append = True
            elif int(rank) != int(value_rank):
                _append = True
        else:
            _append = True

        if _append:
            if name:
                self._append(name, id, rank)
                tag_name = name.replace('`', "'").strip()
                redis.hset(ID2NAME, id, '%s`%s'%(tag_name, rank))
                self._name2id_set(name,id )
            else:
                redis.hdel(NAME2ID, name)

    def _name2id_set(self, name, id):
        NAME2ID = self.NAME2ID
        if not redis.hget(NAME2ID, name):
            redis.hset(NAME2ID, name, id)

    def id_by_name(self, name):
        return redis.hget(self.NAME2ID, name)
         
    def _key(self, name):
        from zkit.pinyin import pinyin_list_by_str

        tag_name = name.lower().replace('/', ' ').strip()

        if not tag_name:
            return


        for sub_tag in tag_name.split(' '):
            for pos in xrange(1, len(sub_tag)+1):
                key = sub_tag[:pos]
                yield key

            pylist = pinyin_list_by_str(sub_tag)
            for py in pylist:
                yield py

            for pos in xrange(2, len(pylist)+1):
                yield ''.join(pylist[:pos])

    def pop_alias(self, name, id):
        ZSET_CID = self.ZSET_CID
        for i in self._key(name):
            redis.zrem(ZSET_CID%i, id)

    def _append(self, name, id, rank=1):
        CACHE = self.CACHE
        ZSET_CID = self.ZSET_CID
        for i in self._key(name):
            redis.delete(CACHE%i)
            #print ZSET_CID%i, id, rank
            redis.zadd(ZSET_CID%i, id, rank)

    def add(self, name, id, rank=1):
        name = name.lower().strip()
        redis.zadd(self.ZSET_CID%name, id, rank)

    def id_list_by_str(self, query, limit=7):
        name_list = query.replace('`', "'").split()
        if not name_list:
            return []

        name_list.sort()

        name_key = '`'.join(name_list)
        id_list = self._get_cache(name_key)

        id_list = None #TODO REMOVE
        ZSET_CID = self.ZSET_CID

        if id_list is None:
            mkey = ZSET_CID%name_key

            if len(name_list)>1 and not redis.exists(mkey):
                p = redis.pipeline()
                p.zinterstore(mkey, map(ZSET_CID.__mod__, name_list), 'MAX')
                p.expire(mkey, EXPIRE)
                p.execute()


            id_list = redis.zrevrange(mkey, 0, 10)

            id_list = list(map(int, id_list))

            #id = self.id_by_name(query)
            #if id:
            #    id = int(id)
            #    if len(id_list) > 5:
            #        id_list.insert(4, id)
            #    else:
            #        id_list.append(id)
 
            #id_list = unique(id_list)
            
            self._set_cache(name_key, id_list)
            
            #print redis.zrevrange(mkey, 0, 10,True)
            #print id_list

        return id_list[:limit]


    def id_rank_name_list_by_str(self, query, limit=7):
        query = query.strip().lower()
        result = []
        id_list = self.id_list_by_str(query, limit)
        #print id_list
        if id_list:
            for id, name_rank in zip(id_list, redis.hmget(self.ID2NAME, id_list)):
                name, rank = name_rank.rsplit('`', 1)
                if query not in name.lower():
                    alias = self.alias_by_id_query(id, query) or 0
                else:
                    alias = 0
                result.append(
                    (id, rank, name, alias)
                )
        return result

    def rank_update(self, id , rank):
        name_rank = redis.hget(self.ID2NAME, id)
        if name_rank:
            name, _rank = name_rank.rsplit('`', 1)
            self.append(name, id, rank)
            for i in tag_alias_by_id_query(id):
                self.append_alias(i, id , rank)

from po_tag import tag_alias_by_id_query
autocomplete_tag = AutoComplete('tag', tag_alias_by_id_query)


if __name__ == '__main__':
    pass
    from model.zsite import Zsite
    from model.cid import CID_TAG, CID_USER
    from zweb.orm import ormiter
    from model.follow import follow_count_by_to_id
    from model.zsite_fav import zsite_fav_count_by_zsite
    from model.po_tag import _tag_alias_new

    
    
    for i in ormiter(Zsite, 'cid=%s'%CID_TAG):
        for j in i.name.split("/"):
            j = j.strip()
            if j != i.name:
                for k in Zsite.where(cid=CID_TAG, name=j):
                    k.name = ""
                    k.save()

    for i in ormiter(Zsite, 'cid=%s'%CID_TAG):
        count = zsite_fav_count_by_zsite(i)
        autocomplete_tag.rank_update(i.id, count)
        for j in i.name.split("/"):
            j = j.strip()
            if j != i.name:
                _tag_alias_new(i.id, j)
                #autocomplete_tag.append_alias(j, i.id, count)

    #from model.autocomplete_user import autocomplete_user 
    #for i in ormiter(Zsite, 'cid=%s'%CID_USER):
    #    count = follow_count_by_to_id(i.id)
    #    print i.id
    #    autocomplete_user.rank_update(i.id, count)

    #print autocomplete_tag.id_rank_name_list_by_str('乔', 14)

    #autocomplete_tag = AutoComplete('tag')
    #autocomplete_tag.append('Facebook/F8', 76514)
    #autocomplete_tag.append('flask', 76515)
    #for i in autocomplete_tag.id_name_list_by_key("f"):
    #    print i
    #print "=+++"

    #from zkit.pprint import pprint
    #pprint(autocomplete_tag.id_rank_name_list_by_str('baidu'))
    #print autocomplete_tag.id_rank_name_list_by_str('f')
    #print redis.keys('tag`baidu')
    #from timeit import timeit
    #def f():
    #    autocomplete_tag.id_name_list_by_name_list('t')

    #print timeit(f,number=10000)/10000
