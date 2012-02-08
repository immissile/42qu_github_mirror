#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from functools import partial
from zkit.pinyin import pinyin_list_by_str

REDIS_ZSET_CID = 'RED_ZSET:%s'
REDIS_TRIE = 'RED_TRIE:%s'
REDIS_ID2NAME = 'RED_ID2NAME%s'
REDIS_CACHE = 'RED_TAGCACHE%s'

TAG_NEW_MODEL_ADD_NEW = 1
TAG_NEW_MODEL_CHANGE2ZSET = 2

__metaclass__ = type

class AutoComplete:
    def __init__(self, key):
        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
        self.TRIE = '%s'%(REDIS_TRIE%name)
        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
        self.CACHE = '%s%%s'%(REDIS_CACHE%name)
    
    def append(self, name, id , rank=1):
        tag_name = name.replace('`', "'").strip()
        redis.hset(self.ID2NAME, id, '%s`%s'%(tag_name,rank))
        
        tag_name = tag_name.lower().replace('/', ' ').strip()
                
        if not tag_name:
            return

        total_list = tag_name.split(" ")

        ZSET_CID = self.ZSET_CID

        zset_list = []
        ztrie_rm_list = []
        ztrie_new_list = []

        for sub_tag in total_list:
            sub_tag_len = len(sub_tag)
            for pos in xrange(1, sub_tag_len+1):
                sub_str = sub_tag[:pos]

                if not ztrie_rm_list and not ztrie_new_list:
                    key = ZSET_CID%sub_str
                    if redis.exists(key):
                        redis.zadd(key, id, rank)
                        continue

                if not ztrie_new_list:
                    start = redis.zrank(self.TRIE, sub_str)
                    if start is not None: #已经存在, 删除
                        ztrie_rm_list.append(sub_str) 
                        continue

                ztrie_new_list.append(sub_str) 
                    



#from time import time
#class profile():
#    begin = None
#    threshold = 0.01
#
#    @staticmethod
#    def start(thre=0.01):
#        profile.threshold = thre
#        profile.begin = time()
#    @staticmethod
#    def end():
#        etime = time()-profile.begin
#        if etime > profile.threshold:
#            print etime, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
#
#def trie_handle_entry(entry):
#    if entry.endswith('`'):
#        entry = entry.split('`')
#        return tuple(entry[:2])
#
#
#class TagSet(object):
#    def __init__(self, name):
#        self.name = name
#
#        self.ZSET_CID = '%s%%s'%(REDIS_ZSET_CID%name)
#        self.TRIE = '%s'%(REDIS_TRIE%name)
#        self.ID2NAME = '%s'%(REDIS_ID2NAME%name)
#        self.CACHE = '%s%%s'%(REDIS_CACHE%name)
#
#    def _set_cache(self, key, name_value_list):
#        key = self.CACHE%key
#        for result in name_value_list:
#            redis.sadd(key, result)
#        redis.expire(key, 86400)
#
#    def _get_cache(self, key):
#        key = self.CACHE%key
#        return redis.smembers(key)
#
#    def tag_fav(self, id, name=None):
#        old_name = self._tag_id2name(id)
#        if old_name:
#            name, rank = old_name
#            rank = int(rank) + 1
#            new_name = '`'.join([name, str(rank)])
#            redis.hset(self.ID2NAME, id, new_name)
#        elif name:
#            redis.hset(self.ID2NAME, id, '%s`1'%name)
#
#    def _tag_id_list2result(self, id_list):
#        result_list = []
#        for id in id_list:
#            name, rank = self._tag_id2name(id)
#            result_list.append((name, id, rank))
#
#        result_list.sort(key=lambda x:x[2], reverse=True)
#        return result_list
#
#    def tag_new(self, tag_name, id, rank=1):
#        tag_name = tag_name.replace('`', "'").strip()
#        redis.hset(self.ID2NAME, id, '%s`%s'%(tag_name,rank))
#        
#        tag_name = tag_name.lower().replace('/', ' ').strip()
#
#        if not tag_name:
#            return
#
#        model = None
#
#        total_list = tag_name.split(" ")
#
#        ZSET_CID = self.ZSET_CID
#        for sub_tag in total_list:
#            sub_tag_len = len(sub_tag)
#            for pos in xrange(1, sub_tag_len+1):
#                sub_str = sub_tag[:pos]
#
#                old_name_list = self._tag_from_trie(sub_str)
#                if old_name_list:
#                    old_name_list = self._tag_id_list2result(old_name_list)
#                    old_name_list = old_name_list[0][0].lower().split('/')
#
#                key = ZSET_CID%sub_str
#                 
#
#            #first_char = sub_tag[0]
#            
#            #if redis.zscore(self.TRIE, first_char) is not None:
#            #    model = TAG_NEW_MODEL_CHANGE2ZSET
#            #else:
#            #    model = TAG_NEW_MODEL_ADD_NEW
#
#            #if model == TAG_NEW_MODEL_CHANGE2ZSET:
#            #    self._trie2zset(sub_tag)
#            #    if sub_tag in old_name_list:
#            #        key = REDIS_ZSET_CID%sub_tag
#            #        redis.zadd(key, id, 1)
#            #    else:
#            #        self._trie_tag_new(sub_tag)
#            #        self._trie_tag_new('%s`%s`'%(sub_tag, id))
#
#            #using_set = False
#            #for pos in range(1, len(sub_tag)):
#            #    sub_str = sub_tag[:pos]
#            #    key = self.ZSET_CID%sub_str
#
#            #    if model == TAG_NEW_MODEL_ADD_NEW:
#            #        self._trie_tag_new(sub_str)
#
#            #    if model == TAG_NEW_MODEL_CHANGE2ZSET:
#
#            #        for old_name in old_name_list:
#            #            if old_name.startswith(sub_str):
#            #                using_set = True
#            #                break
#
#            #        if using_set:
#            #            redis.zadd(key, id, 1)
#            #        else:
#            #            self._trie_tag_new(sub_str)
#            #if model == TAG_NEW_MODEL_CHANGE2ZSET:
#            #    if using_set:
#            #        key = self.ZSET_CID%sub_tag
#            #        redis.zadd(key, id, 1)
#            #    else:
#            #        self._trie_tag_new('%s`%s`'%(sub_tag, id))
#
#            #if model == TAG_NEW_MODEL_ADD_NEW:
#            #    self._trie_tag_new(sub_tag)
#            #    self._trie_tag_new('%s`%s`'%(sub_tag, id))
#
#
#    def tag_by_name_list(self, name_list_str):
#        name_list = name_list_str.strip().lower().split()
#        name_list.sort()
#
#        key = '-'.join(name_list)
#        result_list = self._get_cache(key)
#        result_list = None
#
#        if result_list is None:
#            result_list = reduce(
#                set.intersection, map(
#                    set,map(
#                        self.tag_id_list_by_name,
#                        name_list
#                    )
#                )
#            )
#            self._set_cache(key, result_list)
#
#        return self._tag_id_list2result(result_list)
#
#    def tag_id_list_by_name(self, name):
#        name = name.decode("utf-8","ignore")
#        result_list = []
#        key = self.ZSET_CID%name
#        if redis.exists(key):
#            result_list = redis.zrevrange(key, 0, -1)
#        elif redis.zscore(self.TRIE, name) is not None:
#            result_list = self._tag_from_trie(name)
#        return result_list
#
#    def tag_by_name(self, name):
#        name = name.lower()
#        id_list = self.tag_id_list_by_name(name)
#        return self._tag_id_list2result(id_list)
#
#    def _trie2zset(self, name):
#        first_char = name[0]
#        id = self._tag_from_trie(first_char)[0]
#        for i in self._trie_name_id_iter(first_char, ):
#            yield self._trie2zset_iter_handler, id=id, new_name=name)
#
#    def _trie2zset_iter_handler(self, key, id, new_name):
#        if new_name.startswith(key):
#            redis.zrem(self.TRIE, key)
#
#            if key.endswith('`'):
#                key = key.split('`')[0]
#
#            key = self.ZSET_CID%key
#            redis.zadd(key, id , 1)
#
#    def _trie_tag_new(self, name):
#        if name:
#            redis.zadd(self.TRIE, name, 0)
#
#    def _tag_id2name(self, id):
#        result = redis.hget(self.ID2NAME, int(id))
#        if result:
#            return result.split('`')
#
#    def _trie_key_iter(self, prefix):
#        rangelen = 20
#        start = redis.zrank(self.TRIE, prefix)
#        result = None
#        while start is not None:
#            r = redis.zrange(self.TRIE, start, start + rangelen - 1)
#            rlen = len(r)
#            start += rlen
#            if not rlen:
#                return 
#            for entry in r:
#                if not entry.startswith(prefix):
#                    return
#                yield entry
# 
#
#    def _trie_name_id_iter(self, prefix):
#
#
#        for i in self._trie_key_iter(prefix):
#            yield i[:-1].rsplit('`',1)
#        #        else:
#        #            result = callback(entry)
#        #    if signal:break
#        #if result:
#        #    return [result[1]]
#
#    def _tag_from_trie(self, prefix):
#        for i in self._trie_name_id_iter(prefix):
#            yield trie_handle_entry(i)
#
#tag_tag = TagSet('tag')
#
#def rm():
#    redis.DEL(REDIS_TRIE)
#
#if __name__ == '__main__':
#    #tag_tag = TagSet('po')
#    tag_tag.tag_new('Facebook/F8', 76514)
#    #tag_tag.tag_new('jobs', 123)
#    #tag_tag.tag_new('steve/jobs', 334423)
#    #tag_tag.tag_new('/'.join(['新浪微博', 'VS', 'Twitter']), 10010)
#    #tag_tag.tag_new('/'.join(['蒂姆', '库克', 'Tim', 'Cook']), 881009)
#    ##tag_tag.tag_new('火', 0)
#    ##tag_tag.tag_new('火车', 1)
#    ##tag_tag.tag_new('火柴', 2)
#    #print redis.zscore(REDIS_TRIE,'stev')
#    #for i in _tag_from_trie('j'):
#    #    print list(i)
#    #print '/'.join(i)
#    #print redis.zrange(REDIS_TRIE,0,-1)
#    #redis.keys()
#    #print _tag_from_trie('史')[0][0]
#    #print tag_tag.tag_by_name_list('fe')
#    #print tag_tag.tag_by_name('Tim')
#
#    #from timeit import timeit
#    #def f():
#    #    tag_tag.tag_by_name('t')
#
#    #print timeit(f,number=10000)/10000
#    #tag_tag.tag_fav(881009)
#    #print tag_tag.tag_by_name_list('s Co')
#    #print tag_tag.tag_by_name('C')
#    #print tag_tag.tag_by_name('新')
#    pass
