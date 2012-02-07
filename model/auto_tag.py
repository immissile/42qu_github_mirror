#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import redis
from functools import partial

REDIS_ZSET_CID = 'RED_ZSET:%s'
REDIS_TRIE = 'RED_TRIE'
REDIS_ID2NAME = 'RED_ID2NAME'

TAG_NEW_MODEL_ADD_NEW = 1
TAG_NEW_MODEL_INC_ZSET = 2
TAG_NEW_MODEL_CHANGE2ZSET = 3

def tag_from_zset(name):
    key = REDIS_ZSET_CID%name
    result = redis.zrevrange(key , 0, 6)
    return result

def tag_new(tag_name, id):
    model = None
    for sub_tag in tag_name.split('/'):
        sub_tag = unicode(sub_tag)

        first_char = sub_tag[0]

        if redis.exists(REDIS_ZSET_CID%first_char):
            model = TAG_NEW_MODEL_INC_ZSET
        elif redis.zscore(REDIS_TRIE, first_char) == 0:
            model = TAG_NEW_MODEL_CHANGE2ZSET
        else:
            model = TAG_NEW_MODEL_ADD_NEW

        for pos in range(1, len(sub_tag)):
            sub_str = sub_tag[:pos]
            key = REDIS_ZSET_CID%sub_str

            if model == TAG_NEW_MODEL_ADD_NEW:
                trie_tag_new(sub_str)

            if model == TAG_NEW_MODEL_INC_ZSET:
                #increase sub string value in zset
                redis.zincrby(key, id, 1)

            if model == TAG_NEW_MODEL_CHANGE2ZSET:
                #adding sub strings to zset, remove later
                redis.zadd(key, id, 1)

        if model == TAG_NEW_MODEL_ADD_NEW:
            #final string to trie
            redis.hset(REDIS_ID2NAME, id, tag_name)
            trie_tag_new('%s*%s*'%(sub_tag,id))

        elif model == TAG_NEW_MODEL_INC_ZSET:
            #final key to increase
            key = REDIS_ZSET_CID%sub_tag
            redis.zincrby(key, id, 1)
            pass

        if model == TAG_NEW_MODEL_CHANGE2ZSET:
            #TODO: remove from trie, add final string to zset
            trie2zset(sub_tag)
            key = REDIS_ZSET_CID%sub_tag
            redis.zadd(key, id, 1)

def tag_by_name(name):
    name = unicode(name)
    if redis.exists(REDIS_ZSET_CID%name):
        tag_list = redis.zrevrange(REDIS_ZSET_CID%name, 0, -1, True)
        tag_list = map(lambda x: (tag_id2name(x[0]),x[0]),tag_list)
        return tag_list
    elif redis.zscore(REDIS_TRIE, name[0]) == 0:
        return tag_from_trie(name)
    else:
        return []

def trie2zset(name):
    first_char = name[0]
    id = tag_from_trie(first_char)[0][1]
    trie_iter(first_char, partial(trie2zset_iter_handler, id=id))

def trie2zset_iter_handler(key, id):
    redis.zrem(REDIS_TRIE, key)

    if key.endswith('*'):
        key = key.split('*')[0]

    key = REDIS_ZSET_CID%key
    redis.zadd(key, id , 1)

def trie_tag_new(name):
    redis.zadd(REDIS_TRIE, name, 0)

def tag_id2name(id):
    return redis.hget(REDIS_ID2NAME, id)

def trie_iter(prefix, callback):
    rangelen = 50
    start = redis.zrank(REDIS_TRIE, prefix)
    results = []
    while start != None:
        range = redis.zrange(REDIS_TRIE, start, start + rangelen - 1)
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
                name,id=result[0],result[1]
                results.append((tag_id2name(id), id))
    return results

def trie_handle_entry(entry):
    if entry.endswith('*'):
        entry = entry.split('*')
        return tuple(entry[:2])

def tag_from_trie(prefix):
    prefix = unicode(prefix)
    return trie_iter(prefix, trie_handle_entry)

def rm():
    redis.DEL(REDIS_TRIE)

if __name__ == '__main__':
    #tag_new('史蒂夫/乔布斯/steve/jobs', 10086)
    #tag_new('/'.join(['新浪微博', 'VS', 'Twitter']), 10010)
    #tag_new('/'.join(['蒂姆', '库克', 'Tim', 'Cook']), 881009)
    #print redis.zscore(REDIS_TRIE,'stev')
    #for i in tag_from_trie('j'):
    #    print list(i)
    #print '/'.join(i)
    #print redis.zrange(REDIS_TRIE,0,-1)
    #redis.keys()
    #print tag_from_trie('史')[0][0]
    print tag_by_name('V')
    print tag_by_name('s')
    print tag_by_name('新')
    pass
