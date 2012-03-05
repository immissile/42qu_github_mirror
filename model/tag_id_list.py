#coding:utf-8

from _db import redis

#标签汇总 - 用户数
#标签%id - 用户 id list 
#用户%id - 标签 id list

#标签汇总 - 文章数
#文章%id - 标签 id list
#标签%id - 文章 id list


class Tag2IdList(object):
    def __init__(self, prefix):
        self.key_tag_count = 'T-I.SUM#%s:%%s'%prefix            #zset 
        self.key_tag_id_xid_list = 'T2I.%s:%%s'%prefix          #list
        self.key_xid_tag_id_list = 'I2T.%s:%%s'%prefix          #list 

    def append_id_tag_id_list(self, id, tag_id_list):
        if not id or not tag_id_list:
            return
        key_tag_id_xid_list = self.key_tag_id_xid_list
        key_xid_tag_id_list = self.key_xid_tag_id_list%id

        tag_id_set = set(tag_id_list)
        key_list = []
        p = redis.pipeline()

        for tag_id in tag_id_set:
            p.lrem(key_xid_tag_id_list, tag_id)
            p.lpush(key_xid_tag_id_list, tag_id)

            key = key_tag_id_xid_list%tag_id
            p.lrem(key, id)
            p.lpush(key, id)

        p.execute()

        self._flush_count(tag_id_set)

    def _flush_count(self, tag_id_set):
        key_tag_id_xid_list = self.key_tag_id_xid_list
        key_tag_count = self.key_tag_count

        for tag_id in tag_id_set:
            key = key_tag_id_xid_list%tag_id
            redis.zadd(key_tag_count, tag_id, redis.llen(key))


    def pop_id(self, id):
        key_tag_id_xid_list = self.key_tag_id_xid_list
        key_xid_tag_id_list = self.key_xid_tag_id_list%id

        tag_id_set = redis.lrange(key_xid_tag_id_list, 0, -1)

        p = redis.pipeline()
        for tag_id in tag_id_set:
            p.lrem(key_tag_id_xid_list%tag_id, id)
        p.execute()

        redis.delete(key_xid_tag_id_list)

        self._flush_count(tag_id_set)


    def pop_id_tag_id(self, id, tag_id):
        key_tag_id_xid_list = self.key_tag_id_xid_list
        key_xid_tag_id_list = self.key_xid_tag_id_list%id

        p = redis.pipeline()
        p.lrem(key_tag_id_xid_list%tag_id, id)
        p.lrem(key_xid_tag_id_list, tag_id)
        p.execute()

        self._flush_count(tag_id_set)

    def id_list_by_tag_id(self, tag_id, limit=None, offset=0):
        key = self.key_tag_id_xid_list%tag_id
        if limit is None:
            end = -1
        else: 
            end = offset+limit-1
        return redis.lrange(key, offset, end)

    def tag_id_list_by_id(self, id):
        key = self.key_xid_tag_id_list%id 
        return redis.lrange(key, 0, -1)


if __name__ == "__main__":
    pass

    t = Tag2IdList('T')
    print t.id_list_by_tag_id(2)


