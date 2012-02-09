#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from zkit.zitertools import lineiter
from zkit.pinyin import pinyin_list_by_str

REDIS_ZSET_CID = '%s`'
REDIS_TRIE = 'RED_TRIE:%s'
REDIS_ID2NAME = 'RED_ID2NAME%s'
REDIS_CACHE = 'RED_TAGCACHE%s'


__metaclass__ = type

class AutoComplete:
    def __init__(self, name):
        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.TRIE = '%s'%(REDIS_TRIE%name)
        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
        self.CACHE = '%s%%s'%(REDIS_CACHE%name)

    def _set_cache(self, key, name_value_list):
        key = self.CACHE%key
        for result in name_value_list:
            redis.sadd(key, result)
        redis.expire(key, 86400)

    def _get_cache(self, key):
        key = self.CACHE%key
        return redis.smembers(key)

    def _id_rank_by_prefix_from_trie(self, prefix):
        id_list = self.id_list_by_key(prefix)
        result = [x[:2] for x in self._id_rank_name_by_prefix_from_trie(id_list)]

        return result

    def _id_rank_name_by_prefix_from_trie(self, id_list):
        result = []

        if id_list:
            for id, name_rank in zip(id_list, redis.hmget(self.ID2NAME, id_list)):
                name, rank = name_rank.rsplit('`', 1)
                result.append((id, rank, name))

        return result

    def append(self, name, id , rank=1):
        name = name.decode('utf-8','ignore')
        ID2NAME = self.ID2NAME

        value = redis.hget(ID2NAME, id)
        if value:
            #TODO 如果rank不一样, 需要进行修改
            #TODO 如果name不一样, 需要删除然后重新索引
            return

        tag_name = name.replace('`', "'").strip()
        redis.hset(ID2NAME, id, '%s`%s'%(tag_name, rank))

        tag_name = tag_name.lower().replace('/', ' ').strip()

        if not tag_name:
            return

        total_list = tag_name.split(' ')

        ZSET_CID = self.ZSET_CID
        TRIE = self.TRIE

        ztrie_not_rmed = True
        ztrie_not_newed = True

        for sub_tag in total_list:
            sub_tag_len = len(sub_tag)
            for pos in xrange(1, sub_tag_len+1):
                sub_str = sub_tag[:pos]

                if ztrie_not_newed:
                    key = ZSET_CID%sub_str

                if ztrie_not_rmed and ztrie_not_newed:
                    if redis.exists(key):
                        redis.zadd(key, id, rank)
                        continue
                    else:
                        ztrie_not_rmed = False

                if ztrie_not_newed:

                    start = redis.zrank(TRIE, sub_str)
                    if start is not None: #已经存在, 删除

                        olist = [x[:2] for x in self._id_rank_by_prefix_from_trie(sub_str)]
                        olist.append((id, rank))

                        p = redis.pipeline()
                        p.zadd(key, *lineiter(olist))
                        p.zrem(TRIE, sub_str)
                        p.execute()

                        continue
                    else:
                        ztrie_not_newed = False

                if pos == sub_tag_len:
                    redis.zadd(TRIE, sub_str, 0)
                    sub_str = '%s`%s`'%(sub_str, id)

                redis.zadd(TRIE, sub_str, 0)

    def _trie_key_iter(self, prefix):
        rangelen = 50
        start = redis.zrank(self.TRIE, prefix)
        try:
            while start is not None:
                r = redis.zrange(self.TRIE, start, start + rangelen - 1)
                rlen = len(r)
                start += rlen
                if not rlen:
                    break
                for entry in r:
                    if not entry.startswith(prefix):
                        raise StopIteration
                    if entry.endswith('`'):
                        yield entry
        except StopIteration:
            pass


    def _trie_name_id_iter(self, prefix):
        return [i[:-1].rsplit('`', 1)[1] for i in self._trie_key_iter(prefix)]

    def id_list_by_key(self, key):
        id_list = []
        cid_key = self.ZSET_CID%key

        if redis.exists(cid_key):
            id_list = redis.zrevrange(cid_key, 0, -1)

        elif redis.zrank(self.TRIE, key) is not None:
            id_list = self._trie_name_id_iter(key)

        return id_list

    def id_name_list_by_key(self, key):
        key = key.lower()
        id_list = self.id_list_by_key(key)
        return  self._id_rank_name_by_prefix_from_trie(id_list)

    def tag_by_name_list(self, name_list_str):
        name_list = name_list_str.strip().lower().split()
        name_list.sort()

        key = '-'.join(name_list)
        result_list = self._get_cache(key)
        result_list = None

        if result_list is None:
            result_list = reduce(
                set.intersection, map(
                    set, map(
                        self.id_list_by_key,
                        name_list
                    )
                )
            )
            self._set_cache(key, result_list)

        return result_list

    def id_name_list_by_name_list(self, name_list_str):
        return self._id_rank_name_by_prefix_from_trie(self.tag_by_name_list(name_list_str))
    
auto_complete_tag = AutoComplete('tag')

if __name__ == '__main__':
    pass
    #auto_complete_tag = AutoComplete('tag')
    #auto_complete_tag.append('Facebook/F8', 76514)
    #auto_complete_tag.append('flask', 76515)
    #for i in auto_complete_tag.id_name_list_by_key("f"):
    #    print i
    #print "=+++"

    print auto_complete_tag.id_name_list_by_name_list("f f8")

    #from timeit import timeit
    #def f():
    #    auto_complete_tag.id_name_list_by_name_list('t')

    #print timeit(f,number=10000)/10000
