#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import redis
from functools import partial

REDIS_ZSET_CID = 'RED_ZSET:%s'
REDIS_TRIE = 'RED_TRIE:%s'
REDIS_ID2NAME = 'RED_ID2NAME%s'
REDIS_CACHE = 'RED_TAGCACHE%s'

TAG_NEW_MODEL_ADD_NEW = 1
TAG_NEW_MODEL_INC_ZSET = 2
TAG_NEW_MODEL_CHANGE2ZSET = 3


def trie_handle_entry(entry):
    if entry.endswith('*'):
        entry = entry.split('*')
        return tuple(entry[:2])


class TagSet(object):
    def __init__(self, name):
        self.name = name

        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.TRIE = '%s'%(REDIS_TRIE%name)
        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
        self.CACHE = '%s%%s'%(REDIS_CACHE%name)

    def set_cache(self,key, name_value_list):
        key = self.CACHE%key
        for result, rank in name_value_list:
            redis.zadd(key, result, rank)
        redis.expire(key, 1800)

    def tag_fav(self, id, name=None):
        old_name = self.tag_id2name(id)
        if old_name:
            name, rank = old_name
            rank = int(rank) + 1
            new_name = '*'.join([name, str(rank)])
            redis.hset(self.ID2NAME, id, new_name)
        elif name:
            redis.hset(self.ID2NAME, id, '%s*1'%name)

    def tag_id_list2_result(self, id_list):
        results = []
        for id, zrank in id_list:
            name, rank = self.tag_id2name(id)
            results.append((name, id, rank))

        results.sort(key=lambda x:x[2], reverse=True)
        return results

    def tag_new(self, tag_name, id):
        if not tag_name.strip():
            return

        model = None
        for sub_tag in tag_name.split('/'):
            sub_tag = unicode(sub_tag).lower()

            first_char = sub_tag[0]

            old_name_list = self.tag_from_trie(first_char)
            if old_name_list:
                old_name_list = self.tag_id_list2_result(old_name_list)
                old_name_list = old_name_list[0][0].lower().split('/')

            if redis.exists(self.ZSET_CID%sub_tag):
                model = TAG_NEW_MODEL_INC_ZSET
            elif redis.zscore(self.TRIE, first_char) != None:
                model = TAG_NEW_MODEL_CHANGE2ZSET
            else:
                model = TAG_NEW_MODEL_ADD_NEW

            if model == TAG_NEW_MODEL_CHANGE2ZSET:
                #TODO: remove from trie, add final string to zset
                self.trie2zset(sub_tag)
                if sub_tag in old_name_list:
                    key = REDIS_ZSET_CID%sub_tag
                    redis.zadd(key, id, 1)
                else:
                    self.trie_tag_new(sub_tag)
                    self.trie_tag_new('%s*%s*'%(sub_tag, id))

            for pos in range(1, len(sub_tag)):
                sub_str = sub_tag[:pos]
                key = self.ZSET_CID%sub_str

                if model == TAG_NEW_MODEL_ADD_NEW:
                    self.trie_tag_new(sub_str)

                if model == TAG_NEW_MODEL_INC_ZSET:
                    #increase sub string value in zset
                    redis.zincrby(key, id, 1)

                if model == TAG_NEW_MODEL_CHANGE2ZSET:
                    #adding sub strings to zset, remove later
                    using_set = False

                    for old_name in old_name_list:
                        if old_name.startswith(sub_str):
                            using_set = True
                            break

                    if using_set:
                        redis.zadd(key, id, 1)
                    else:
                        self.trie_tag_new(sub_str)


            if model == TAG_NEW_MODEL_ADD_NEW:
                #final string to trie
                #redis.hset(self.ID2NAME, id, tag_name)
                self.trie_tag_new(sub_tag)
                self.trie_tag_new('%s*%s*'%(sub_tag, id))

            elif model == TAG_NEW_MODEL_INC_ZSET:
                #final key to increase
                key = self.ZSET_CID%sub_tag
                redis.zincrby(key, id, 1)
                pass

        if model == TAG_NEW_MODEL_ADD_NEW or model==TAG_NEW_MODEL_CHANGE2ZSET:
            redis.hset(self.ID2NAME, id, '%s*1'%tag_name)
            
    def set(self,name,id):
        redis.hset(self.ID2NAME, id, '%s*1'%name)

    def tag_from_zset_by_key(self, key):
        return redis.zrevrange(key, 0, -1, True)

    def tag_by_name_list(self, name_list_str):
        name_list = name_list_str.strip().lower().split()
        name_list.sort()

        key = '-'.join(name_list)
        results = redis.zrevrange(key, 0, -1, True)

        if not results:
            results = dict()
            for name in name_list:
                for tag in self.tag_id_list_by_name(name):
                    id = str(tag[0])
                    if id not in results:
                        results[id] = tag[1]

            results = results.items()
            self.set_cache(key, results)

        return self.tag_id_list2_result(results)


    def tag_id_list_by_name(self, name):
        name = unicode(name)
        results = []
        if redis.exists(self.ZSET_CID%name):
            results = self.tag_from_zset_by_key(self.ZSET_CID%name)
        elif redis.zscore(self.TRIE, name) != None:
            results = self.tag_from_trie(name)
        return results

    def tag_by_name(self, name):
        name = name.lower()
        id_list = self.tag_id_list_by_name(name)
        return self.tag_id_list2_result(id_list)

    def trie2zset(self, name):
        first_char = name[0]
        id = self.tag_from_trie(first_char)[0][0]
        self.trie_iter(first_char, partial(self.trie2zset_iter_handler, id=id, new_name=name))

    def trie2zset_iter_handler(self, key, id, new_name):
        if new_name.startswith(key):
            redis.zrem(self.TRIE, key)

            if key.endswith('*'):
                key = key.split('*')[0]

            key = self.ZSET_CID%key
            redis.zadd(key, id , 1)

    def trie_tag_new(self, name):
        if name:
            redis.zadd(self.TRIE, name, 0)

    def tag_id2name(self, id):
        result = redis.hget(self.ID2NAME, int(id))
        if result:
            return result.split('*')

    def trie_iter(self, prefix, callback):
        rangelen = 50
        start = redis.zrank(self.TRIE, prefix)
        results = []
        while start != None:
            range = redis.zrange(self.TRIE, start, start + rangelen - 1)
            start += rangelen
            if not range or len(range) == 0:
                break
            for entry in range:
                entry = unicode(entry)
                minlen = min((len(entry), len(prefix)))
                if entry[0:minlen] != prefix[0:minlen]:
                    break
                result = callback(entry)
                if result:
                    name, id = result[0], result[1]
                    results.append((id, 0))
        return results

    def tag_from_trie(self, prefix):
        prefix = unicode(prefix)
        return self.trie_iter(prefix, trie_handle_entry)

tag_tag = TagSet('tag')

def rm():
    redis.DEL(REDIS_TRIE)

if __name__ == '__main__':
    #tag_tag = TagSet('po')
    #tag_tag.tag_new('史蒂夫/乔布斯/steve/jobs', 10086)
    #tag_tag.tag_new('火', 0)
    #tag_tag.tag_new('火车', 1)
    #tag_tag.tag_new('火柴', 2)
    #tag_tag.tag_new('/'.join(['新浪微博', 'VS', 'Twitter']), 10010)
    #tag_tag.tag_new('/'.join(['蒂姆', '库克', 'Tim', 'Cook']), 881009)
    #print redis.zscore(REDIS_TRIE,'stev')
    #for i in tag_from_trie('j'):
    #    print list(i)
    #print '/'.join(i)
    #print redis.zrange(REDIS_TRIE,0,-1)
    #redis.keys()
    #print tag_from_trie('史')[0][0]
    #print tag_tag.tag_by_name('Tw')
    #print tag_tag.tag_by_name('T')

    from timeit import timeit
    def f():
        tag_tag.tag_by_name('t')

    print timeit(f,number=10000)/10000
    #tag_tag.tag_fav(881009)
    #print tag_tag.tag_by_name_list('s Co')
    #print tag_tag.tag_by_name('C')
    #print tag_tag.tag_by_name('新')
    pass
