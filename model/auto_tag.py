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

    def _id_rank_by_prefix_from_trie(self, prefix):
        id_list = []

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
                    elif entry.endswith('`'):
                        id_list.append(entry[:-1].rsplit('`', 1)[1])
        except StopIteration:
            pass

        result = []

        for id, name_rank in zip(id_list, redis.hmget(self.ID2NAME, id_list)):
            rank = name_rank.rsplit('`', 1)[-1]
            result.append((id, rank))

        return result


    def append(self, name, id , rank=1):
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
                    start = redis.zrank(self.TRIE, sub_str)
                    if start is not None: #已经存在, 删除

                        olist = self._id_rank_by_prefix_from_trie(sub_str)
                        olist.append((id, rank))

                        p = redis.pipeline()
                        p.zadd(key, *lineiter(olist))
                        p.zrem(TRIE, sub_str)
                        p.execute()

                        continue
                    else:
                        ztrie_not_newed = False

                if pos == sub_tag_len:
                    sub_str = '%s`%s`'%(sub_str, id)

                redis.zadd(TRIE, sub_str, 0)

    def id_list_by_key(self):
        pass
    def id_name_list_by_key(self, key):
        id_list = []
        return [ 
            i.rsplit('`', 1)
            for i in
            redis.hmget(self.ID2NAME, id_list)
        ]

if __name__ == '__main__':
    pass


    auto_complete_tag = AutoComplete('tag')
    auto_complete_tag.append('Facebook/F8', 76514)
    auto_complete_tag.append('flask', 76514)



