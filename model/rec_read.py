#coding:utf-8
from _db import McCache, redis
from model.po_json import po_json
from model.days import time_new_offset
from zkit.algorithm.wrandom import wsample2
from zkit.zitertools import lineiter, chunkiter
from array import array
from model.zsite_list import zsite_list, ZsiteList
from model.cid import CID_TAG
from math import log
from time import time
from mq import mq_client
from model.days import ONE_DAY
from random import random

__metaclass__ = type

REDIS_REC_USER_TAG = 'Rec@%s'                 #用户 - 主题 - 分数 zset
REDIS_REC_USER_TAG_CAN_REC = 'Rec?%s'         #用户 - 可以推荐的主题 - 分数 string 
REDIS_REC_TAG_USER_IS_EMPTY = 'Rec~%s'        #主题 - 已经读完了的用户 set
REDIS_REC_TAG = 'RecTag'                      #所有热门主题 用于没有推荐主题的时候随机推荐
REDIS_REC_TAG_ID_SCORE = 'RecTagIdScore'      #所有热门主题 id score的缓存 
REDIS_REC_USER_LOG = 'Rec+%s'                 #用exist判断文章是否已经读过 zset
REDIS_REC_USER_TAG_READED = 'Rec(%s'          #用户 - 主题 - 已经读过的文章
REDIS_REC_USER_TAG_TO_REC = 'Rec)%s'          #用户 - 主题 - 可以推荐的文章的缓存
REDIS_REC_TAG_NEW = 'Rec/%s'                  #话题下的新内容
REDIS_REC_TAG_OLD = 'Rec&%s'                  #话题下的老内容
REDIS_REC_PO_SCORE = 'RecPoScore'             #话题的积分 hset
REDIS_REC_PO_TIMES = 'Rec>%s'                  #老话题的被推荐次数 
REDIS_REC_LAST_TIME = 'RecLastTime'            #上次推荐话题的时间

REDIS_REC_USER_TAG_LIMIT = 512
REDIS_REC_PO_SHOW_TIMES = 10

def rec_read_user_topic_score_incr(user_id, tag_id, score=1):
    key = REDIS_REC_USER_TAG%user_id
    redis.zincrby(key, tag_id, score)
    redis.zincrby(REDIS_REC_TAG, tag_id, score)

    # zrank <  REDIS_REC_USER_TAG_LIMIT的时候 
    # 并且不在读完的redis时候 , 进入主题推荐 
    if redis.zrevrank(key, tag_id) < REDIS_REC_USER_TAG_LIMIT :
        if not redis.sismember(REDIS_REC_TAG_USER_IS_EMPTY%tag_id, user_id):
            _rec_topic_new_by_user_id_topic_id_score(user_id, tag_id)

def rec_read_new(po_id, tag_id):
    mq_rec_topic_has_new(tag_id)
    redis.zadd(REDIS_REC_TAG_NEW%tag_id, po_id, 1)

#@mq_client
def mq_rec_topic_has_new(tag_id):
    rec_topic_has_new(tag_id)


def _po_rec_times_incr(po_id):
    redis.hincrby(REDIS_REC_PO_TIMES, po_id, 1)
    k = random()
    if k < 0.01:
        po_rec_score 


def rec_read_by_user_id_tag_id(user_id, tag_id):
    po_id = 0

    now = time_new_offset()


    #如果有可以推荐的缓存 , 读取缓存
        #增加展示次数, 有1/100的概率更新分数

    #如果 没有新文章 or now - 主题下最近读过的文章的时间戳 < 1个小时 
        #如果没有可以推荐的缓存, 生成缓存, 缓存有效期1天

    #else 推荐新文章 , 增加展示次数 


    return po_id

def po_json_by_rec_read(user_id, limit=8):
    id_list = rec_read_more(user_id, limit)
    return po_json(user_id , id_list, 47)

def rec_read_more(user_id, limit):
    if rec_read(user_id, limit):
        return rec_read_log_by_user_id(user_id, limit, 0)
    return []

def rec_read_log_by_user_id(user_id, limit, offset):
    key = REDIS_REC_USER_LOG%user_id
    return redis.zrevrange(key, offset, offset+limit-1)

def rec_limit_by_time(user_id, limit):
    now = int(time())
    last = redis.hget(REDIS_REC_LAST_TIME, user_id) or 0
    times = int((now - int(last) + 59)//60)
    return min(times, limit)


def dumps_id_score(id_score):
    r = array('I')
    r.fromlist(lineiter(id_score))
    return r.tostring()

def loads_id_score(id_score):
    r = array('I')
    r.fromstring(id_score)
    return list(chunkiter(r, 2))



def rec_topic_has_new(tag_id):
    user_id_list = redis.smembers(REDIS_REC_TAG_USER_IS_EMPTY%tag_id)
    for user_id in user_id_list:
        key = REDIS_REC_USER_TAG%user_id

        rank = redis.zrevrank(key, tag_id)
        if rank is not None and rank < REDIS_REC_USER_TAG_LIMIT:
            _rec_topic_new_by_user_id_topic_id_score(user_id, tag_id)

def _rec_topic_new_by_user_id_topic_id_score(user_id, tag_id):
    score = redis.zscore(REDIS_REC_USER_TAG%user_id, tag_id)
    if score:
        id_score_list = id_score_list_by_user_id(user_id) or []
        id_score_list.append((
            int(tag_id), int(score)
        ))
        id_score_list_new(user_id, id_score_list)

def id_score_list_by_hot():
    result = redis.get(REDIS_REC_TAG_ID_SCORE)
    if result is None:
        result = redis.zrevrange(REDIS_REC_TAG, 0, REDIS_REC_USER_TAG_LIMIT-1, True)
        result = result.items()
        redis.setex(REDIS_REC_TAG_ID_SCORE, dumps_id_score(result), ONE_DAY)
    else:
        result = loads_id_score(result)
    return result

def id_score_list_by_user_id(user_id):
    key = REDIS_REC_USER_TAG_CAN_REC%user_id

    result = redis.get(key)

    if result is None:
        key_tag = REDIS_REC_USER_TAG%user_id
        if redis.exists(key_tag): #第一次初始化
            r = redis.zrevrange(key_tag, 0, REDIS_REC_USER_TAG_LIMIT-1, True)
            result = r.items()
            id_score_list_new(user_id, result)
        else:
            result = None
    else:
        result = loads_id_score(result)

    return result


def id_score_list_new(user_id, id_score_list):
    key = REDIS_REC_USER_TAG_CAN_REC%user_id
    redis.set(key, dumps_id_score(id_score_list))


class RecTagPicker:
    def __init__(self, user_id):
        self._tag_id_score_list = id_score_list_by_user_id(user_id)
        self._init_sample()
        self.user_id = user_id

    def delete(self, tag_id):
        #print tag_id
        _tag_id_score_list = self._tag_id_score_list

        if _tag_id_score_list is None:
            return

        r = []
        for i in _tag_id_score_list:
            if i[0] == tag_id:
                continue
            r.append(i)

        self._tag_id_score_list = r
        user_id = self.user_id

        id_score_list_new(user_id, r)

        redis.sadd(REDIS_REC_TAG_USER_IS_EMPTY%tag_id, user_id)

        self._init_sample()

    def _init_sample(self):
        _tag_id_score_list = self._tag_id_score_list

        if _tag_id_score_list is None:
            _tag_id_score_list = id_score_list_by_hot()

        if _tag_id_score_list:
            self._choice = wsample2(_tag_id_score_list)
        else:
            self._choice = None

    def __call__(self):
        _choice = self._choice

        if _choice is None:
            return

        return _choice()[0]



def rec_read(user_id, limit):
    limit = rec_limit_by_time(user_id, limit)
    result = []
    if limit > 0:
        picker = RecTagPicker(user_id)
        for i in xrange(limit):

            tag_id = picker()
            if not tag_id:
                break

            po_id = rec_read_by_user_id_tag_id(user_id, tag_id)
            if not po_id:
                picker.delete(tag_id)
                continue

            result.append(po_id)

    if result:
        now = time_new_offset()
        key_log = REDIS_REC_USER_LOG%user_id
        t = []
        offset = 0
        for i in result:
            t.append(i)
            t.append(offset+now)
            offset += 0.01

        redis.zadd(key_log, *t)

    return result


if __name__ == '__main__':
    pass

    user_id = 1000000
    rec_topic_choice = RecTagPicker(user_id)
    for i in xrange(10):
        print rec_topic_choice.choice()

#key = REDIS_REC_USER_TAG%user_id
#redis.delete(key)
#print rec_read_more(user_id, 7)

