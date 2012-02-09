#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from zkit.zitertools import lineiter
from zkit.pinyin import pinyin_list_by_str
from array import array

REDIS_ZSET_CID = '%s`'
REDIS_TRIE = 'ACTrie:%s'
REDIS_ID2NAME = 'ACId2Name:%s'
REDIS_CACHE = 'ACCache:%s'


__metaclass__ = type
EXPIRE = 86400

class AutoComplete:
    def __init__(self, name):
        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.TRIE = '%s'%(REDIS_TRIE%name)
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
        if r:
            t = array('I')
            t.fromstring(r)
        else:
            t = []
        return t


    def _id_rank_name_by_id_list(self, id_list):
        result = []

        if id_list:
            for id, name_rank in zip(id_list, redis.hmget(self.ID2NAME, id_list)):
                name, rank = name_rank.rsplit('`', 1)
                result.append((id, rank, name))

        return result

    def append(self, name, id , rank=1):
        name = name.decode('utf-8', 'ignore')
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

                        id_list = self._trie_name_id_list(sub_str)
                        olist = [x[:2] for x in self._id_rank_name_by_id_list(id_list)]
                        olist.append((id, rank))
                        print olist

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
                if not rlen:
                    break
                start += rlen
                for entry in r:
                    if not entry.startswith(prefix):
                        raise StopIteration
                    if entry.endswith('`'):
                        yield entry
        except StopIteration:
            pass


    def _trie_name_id_list(self, prefix):
        return [i[:-1].rsplit('`', 1)[1] for i in self._trie_key_iter(prefix)]

    def _key_list_inter(self, key_list):
        ZSET_CID = self.ZSET_CID
        if len(key_list) > 1:
            mkey = '-'.join(key_list)
            mkey = ZSET_CID%mkey
            if not redis.exists(mkey):
                p = redis.pipeline()
                p.zinterstore(mkey, map(ZSET_CID.__mod__, key_list), 'MAX')
                p.expire(mkey, EXPIRE*7)
                p.execute()
        else:
            mkey = key_list[0]
            mkey = ZSET_CID%mkey
        return mkey

    def id_list_by_str(self, query, limit=7):
        name_list = query.strip().lower().replace('`', "'").split()
        if not name_list:
            return []

        name_list.sort()

        name_key = '`'.join(name_list)
        id_list = self._get_cache(name_key)
        id_list = None #TODO

        ZSET_CID = self.ZSET_CID
        TRIE = self.TRIE

        if id_list is None:
            key_list = []
            result = []
            for key in name_list:
                cid_key = ZSET_CID%key
                if redis.exists(cid_key):
                    key_list.append(key)
                elif redis.zrank(TRIE, key) is not None:
                    result.append( self._trie_name_id_list(key) )

            if len(key_list) == len(name_list):
                mkey = self._key_list_inter(key_list)
                id_list = redis.zrevrange(mkey, 0, limit)
            else:
                if len(result) > 1:
                    result = reduce(
                        set.intersection, map(
                            set, result
                        )
                    )
                elif result:
                    result = result[0]
                if result:
                    if key_list:
                        mkey = self._key_list_inter(key_list)
                        if result:
                            id_list = []
                            id_list_len = 0
                            for i in result:
                                if redis.zrank(mkey, i): #判断是不是在交集里面
                                    id_list.append(i)
                                    id_list_len += 1
                                    if id_list_len == limit:
                                        break
                        else:
                            id_list = redis.zrevrange(mkey, 0, limit)
                    else:
                        id_list = result
                else:
                    id_list = []

            self._set_cache(name_key, id_list)

        return id_list

        #result_list = None

#        if result_list is None:

        return result_list

    def id_rank_name_list_by_str(self, query):
        return self._id_rank_name_by_id_list(self.id_list_by_str(query))

auto_complete_tag = AutoComplete('tag')

if __name__ == '__main__':
    pass
    #auto_complete_tag = AutoComplete('tag')
    #auto_complete_tag.append('Facebook/F8', 76514)
    #auto_complete_tag.append('flask', 76515)
    #for i in auto_complete_tag.id_name_list_by_key("f"):
    #    print i
    #print "=+++"

    print auto_complete_tag.id_rank_name_list_by_str('f')
    #print auto_complete_tag.id_rank_name_list_by_str('f f8')

    #from timeit import timeit
    #def f():
    #    auto_complete_tag.id_name_list_by_name_list('t')

    #print timeit(f,number=10000)/10000
