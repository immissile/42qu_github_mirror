#coding:utf-8
from _db import McCache, redis
from time import time
from model.po_json import po_json
from model.days import time_new_offset
from zkit.algorithm.wrandom import wsample2
from zkit.zitertools import lineiter, chunkiter
from array import array
from model.zsite_list import zsite_list, ZsiteList
from model.cid import CID_TAG
from math import log


__metaclass__ = type

def dumps_id_rank(id_rank):
    r = array('I')
    r.fromlist(lineiter(id_rank))
    return r.tostring()

def loads_id_rank(id_rank):
    r = array('I')
    r.fromstring(id_rank)
    return list(chunkiter(r, 2))


def tag_rank_by_user_id(user_id):
    c = ZsiteList.raw_sql('select id, rank from zsite_list where cid=%s and owner_id=%s order by rank desc limit 512', CID_TAG, user_id)
    return c.fetchall()


REDIS_REC_LOG = 'Rec-%s'
REDIS_REC_USER_TOPIC = 'Rec@%s'
REC_TOPIC_DEFAULT = tag_rank_by_user_id(0) #TODO
REC_TOPIC_DEFAULT = [(i[0], 1 ) for i in REC_TOPIC_DEFAULT]
REC_TOPIC_DEFAULT_DUMPS = dumps_id_rank(REC_TOPIC_DEFAULT)

def rec_read_new(po_id, tag_id_list):
    pass

#TODO
def rec_read_by_topic(user_id, topic_id):
    return

class RecTopicPicker:
    def __init__(self, user_id):
        key = REDIS_REC_USER_TOPIC%user_id

        result = redis.get(key)

        if result is None:
            result = REC_TOPIC_DEFAULT
            redis.set(key, REC_TOPIC_DEFAULT_DUMPS)
        else:
            result = loads_id_rank(result)

        self._topic_id_rank_list = result
        self._key = key
        self._choice_set()

    def delete(self, topic_id):
        #print topic_id
        r = []
        for i in self._topic_id_rank_list:
            if i[0] == topic_id:
                continue
            r.append(i)

        self._topic_id_rank_list = r
        redis.set(self._key, dumps_id_rank(r))
        self._choice_set()

    def _choice_set(self):
        _topic_id_rank_list = self._topic_id_rank_list
        if _topic_id_rank_list:
            self._choice = wsample2(_topic_id_rank_list)
        else:
            self._choice = None

    def choice(self):
        _choice = self._choice

        if _choice is None:
            return

        return _choice()[0]

def rec_read(user_id, limit):
    now = time_new_offset()

    if limit < 0:
        limit = 0

    t = []
    count = 0
    offset = 0

    rec_topic_choice = RecTopicPicker(user_id)

    while count < limit:

        topic_id = rec_topic_choice.choice()
        if not topic_id:
            break

        po_id = rec_read_by_topic(user_id, topic_id)
        if not po_id:
            #print "delete", topic_id
            rec_topic_choice.delete(topic_id)
            continue

        t.append(po_id)
        t.append(now+offset)

        offset += 0.01
        count += 1

    if count:
        key_log = REDIS_REC_LOG%user_id
        redis.zadd(key_log, *t)

    return count

def rec_read_log_by_user_id(user_id, limit, offset):
    key = REDIS_REC_LOG%user_id
    return  redis.zrevrange(key, offset, offset+limit-1)


def rec_read_more(user_id, limit):
    if rec_read(user_id, limit):
        return rec_read_log_by_user_id(user_id, limit)
    return []

def po_json_by_rec_read(user_id, limit=8):
    id_list = []
    #id_list = rec_read_more(user_id, limit)
    return po_json(user_id , id_list, 47)

if __name__ == '__main__':
    pass

    user_id = 1000000
    rec_topic_choice = RecTopicPicker(user_id)
    for i in xrange(10):
        print rec_topic_choice.choice()

    #key = REDIS_REC_USER_TOPIC%user_id
    #redis.delete(key)
    #print rec_read_more(user_id, 7)

