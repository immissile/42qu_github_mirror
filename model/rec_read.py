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
from model.days import ONE_DAY, ONE_HOUR
from random import random

__metaclass__ = type

REDIS_REC_USER_TAG = 'Rec@%s'                 #用户 - 主题 - 分数 zset
REDIS_REC_USER_TAG_CAN_REC = 'Rec?%s'         #用户 - 可以推荐的主题 - 分数 string 
REDIS_REC_USER_TAG_READED = 'Rec(%s-%s'          #用户 - 主题 - 已经读过的文章
REDIS_REC_USER_PO_TO_REC = 'Rec)%s-%s'           #用户 - 主题 - 可以推荐的文章的缓存
REDIS_REC_TAG_USER_IS_EMPTY = 'Rec~%s'        #主题 - 已经读完了的用户 set

REDIS_REC_USER_LOG = 'Rec+%s'                 #用exist判断文章是否已经读过 zset

REDIS_REC_TAG = 'RecTag'                      #所有热门主题 用于没有推荐主题的时候随机推荐
REDIS_REC_TAG_ID_SCORE = 'RecTagIdScore'      #所有热门主题 id score的缓存 
REDIS_REC_TAG_NEW = 'Rec/%s'                  #话题下的新内容 set
REDIS_REC_TAG_OLD = 'Rec&%s'                  #话题下的老内容
REDIS_REC_PO_SCORE = 'RecPoScore'             #话题的积分 hset
REDIS_REC_PO_TIMES = 'RecTimes'               #老话题的被推荐次数 
REDIS_REC_LAST_TIME = 'RecLastTime'           #上次推荐话题的时间

mc_rec_is_empty = McCache('Rec!%s')

REDIS_REC_USER_TAG_LIMIT = 512
REDIS_REC_PO_SHOW_TIMES = 10

inf = float('inf')
ninf = float('-inf')

def rec_read_user_topic_score_fav(user_id, tag_id):
    rec_read_user_topic_score_incr(user_id, tag_id, score=inf, tag_score=1)

def rec_read_po_tag_rm(po_id, tag_id_list):
    p = redis.pipeline()
    for tag_id in tag_id_list:
        p.zrem(REDIS_REC_TAG_OLD%tag_id, po_id)
        p.srem(REDIS_REC_TAG_NEW%tag_id, po_id)
    p.execute()

def rec_read_po_read_rm(po_id, tag_id_list):
    from model.po_pos import po_viewed_list
    p = redis.pipeline()
    for i in po_viewed_list(po_id):
        p.zrem(REDIS_REC_USER_LOG%i, po_id)
    p.execute()

@mq_client
def mq_rec_read_po_rm(po_id, tag_id_list):
    rec_read_po_rm(po_id, tag_id_list)

def rec_read_user_topic_score_fav_rm(user_id, tag_id):
    rec_read_user_topic_score_incr(user_id, tag_id, score=ninf, tag_score=-1)

#In [14]: redis.zrevrange("Rec@10220175",0,0,True,int)
#[('10234454', 103)]
#
#In [15]: redis.zrevrange("Rec@10220175,1",0,0,True,int)
#[]

def rec_read_user_topic_score_incr(user_id, tag_id, score=1, tag_score=None):
    key = REDIS_REC_USER_TAG%user_id

    if score == inf:
        score_list = redis.zrevrange(key, 0, 0, True, int)
        if score_list:
            score = max(1, score_list[0][1])
        else:
            score = 1
        redis.zadd(key, tag_id, score)
    elif score == ninf:
        redis.zrem(key, tag_id)
    else:
        redis.zincrby(key, tag_id, score)

    if tag_score is None:
        tag_score = score
    redis.zincrby(REDIS_REC_TAG, tag_id, tag_score)

    # zrank <  REDIS_REC_USER_TAG_LIMIT的时候 
    # 并且不在读完的redis时候 , 进入候选的推荐主题
    if redis.zrevrank(key, tag_id) < REDIS_REC_USER_TAG_LIMIT :
        if not redis.sismember(REDIS_REC_TAG_USER_IS_EMPTY%tag_id, user_id):
            _rec_topic_new_by_user_id_topic_id_score(user_id, tag_id)

def rec_read_new(po_id, tag_id):
    mq_rec_topic_has_new(tag_id)
    times = redis.hget(REDIS_REC_PO_TIMES, po_id)
    if times >= REDIS_REC_PO_SHOW_TIMES:
        _user_tag_old_rank(po_id, tag_id, times)
    else:
        redis.sadd(REDIS_REC_TAG_NEW%tag_id, po_id)

@mq_client
def mq_rec_topic_has_new(tag_id):
    rec_topic_has_new(tag_id)


def _user_tag_old_rank(po_id, tag_id, times=None):
    if times is None:
        times = redis.hget(REDIS_REC_PO_TIMES, po_id)

    score = redis.hget(REDIS_REC_PO_SCORE, po_id) or 0
    rank = float(score) / int(times)
    redis.zadd(REDIS_REC_TAG_OLD%tag_id, po_id, rank)


def rec_read_by_user_id_tag_id(user_id, tag_id):
    po_id = 0
    from_new = False
    now = time_new_offset()
    ut_id = (user_id, tag_id)
    key_to_rec = REDIS_REC_USER_PO_TO_REC%ut_id
    key_readed = REDIS_REC_USER_TAG_READED%ut_id
    exists_key_to_rec = redis.exists(key_to_rec)
    cache_key_to_rec = False

    for i in xrange(7):
        #如果有可以推荐的缓存 , 读取缓存
        if exists_key_to_rec:
            po_id_list = redis.zrevrange(key_to_rec, 0, 0)
            if po_id_list:
                po_id = po_id_list[0]
                redis.zrem(key_to_rec, po_id)
            else:
                break
        else:
            key_tag_new = REDIS_REC_TAG_NEW%tag_id
            po_id = redis.srandmember(key_tag_new)
            #print 'srandmember' , po_id
            if po_id:
                from_new = True
                last = redis.zrevrange(key_readed, 0 , 0 , True)
                if last and (last[0][1] - now) < ONE_HOUR:
                    cache_key_to_rec = True
            else:
                cache_key_to_rec = True


        if cache_key_to_rec:
            #生成缓存 有效期1天 推荐文章
            p = redis.pipeline()
            #p = redis
            p.zunionstore(key_to_rec, {key_readed:-1, REDIS_REC_TAG_OLD%tag_id:1})
            p.zremrangebyscore(key_to_rec, '-inf', 0)
            p.expire(key_to_rec, ONE_DAY)
            p.execute()
            exists_key_to_rec = True #方便没有的时候跳出循环

        #print 'redis.zcard(key_readed)', redis.zcard(key_to_rec)

        if po_id:
            redis.zadd(key_readed, po_id, now)
            if redis.zrank(REDIS_REC_USER_LOG%user_id, po_id) is not None:
                po_id = 0

        if po_id:
            break

    if po_id:
        redis.hincrby(REDIS_REC_PO_TIMES, po_id, 1)

        if from_new:
            if redis.hget(REDIS_REC_PO_TIMES, po_id) >= REDIS_REC_PO_SHOW_TIMES:
                redis.srem(key_tag_new, po_id)
                _user_tag_old_rank(po_id, tag_id)
        #else:
                #redis.zincrby(key, po_id, 1)
        else:
            k = random()
            if k < 0.01:
                _user_tag_old_rank(po_id, tag_id)

    return po_id

def po_json_by_rec_read(user_id, limit=7):
    id_list = rec_read_more(user_id, limit)
    return po_json(user_id , id_list, 47)

def rec_read_more(user_id, limit):
    if mc_rec_is_empty.get(user_id) is not None:
        return []

    if rec_read(user_id, limit):
        return rec_read_log_by_user_id(user_id, limit, 0)

    mc_rec_is_empty.set(user_id, '', 600)
    return []

def rec_read_log_by_user_id_auto_more(user_id, limit, offset):
    rec_read(user_id, limit)
    return rec_read_log_by_user_id(user_id, limit, 0)

def rec_read_log_count_by_user_id(user_id):
    key = REDIS_REC_USER_LOG%user_id
    return redis.zcard(key)

def rec_read_log_by_user_id(user_id, limit, offset):
    key = REDIS_REC_USER_LOG%user_id
    return redis.zrevrange(key, offset, offset+limit-1)

def rec_limit_by_time(user_id, limit):
    now = time_new_offset()
    last = redis.hget(REDIS_REC_LAST_TIME, user_id) or 0
    times = int((now - int(last) + 59)//60)
    redis.hset(REDIS_REC_LAST_TIME, user_id, now)
    return min(times, limit)


def dumps_id_score(id_score):
    r = array('I')
    r.fromlist(map(int, lineiter(id_score)))
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
        result = [map(int, i) for i in result]
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
            result = redis.zrevrange(key_tag, 0, REDIS_REC_USER_TAG_LIMIT-1, True)
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

        if tag_id:
            redis.sadd(REDIS_REC_TAG_USER_IS_EMPTY%tag_id, user_id)

        self._init_sample()

    def _init_sample(self):
        _tag_id_score_list = self._tag_id_score_list

        if not _tag_id_score_list:
            _tag_id_score_list = id_score_list_by_hot()

        self._choice = wsample2(_tag_id_score_list)

    def __call__(self):
        _choice = self._choice

        if _choice is None:
            return

        return _choice()[0]



def rec_read(user_id, limit):
    limit = rec_limit_by_time(user_id, limit)
    result = set()
    if limit > 0:
        key_log = REDIS_REC_USER_LOG%user_id
        picker = RecTagPicker(user_id)
        for i in xrange(limit):

            tag_id = picker()
            if not tag_id:
                break

            po_id = rec_read_by_user_id_tag_id(user_id, tag_id)
            if not po_id:
                picker.delete(tag_id)
                continue

            result.add(po_id)

        if result:
            now = time_new_offset()
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


#print time_new_offset()
#from model.po_tag import PoZsiteTag
#for i in redis.zrange(REDIS_REC_TAG,0, -1):
#    redis.zadd(REDIS_REC_TAG, i, PoZsiteTag.where(zsite_id=i).count()) 
#redis.delete(REDIS_REC_TAG_ID_SCORE)

#user_id = 10000000 
#key = REDIS_REC_USER_TAG%user_id
#rec_read_user_topic_score_fav(user_id, 10225249)
#print redis.zrevrange(key, 0, 0, True, int)
#rec_read_user_topic_score_fav_rm(user_id, 10225249)
#print redis.zrevrange(key, 0, 0, True, int)
#    from model.zsite import Zsite
#    for i in Zsite.mc_get_list( redis.zrange(REDIS_REC_TAG,0,-1) ):
#        print i.name
#    user_id = 10000000
#    print po_json_by_rec_read(user_id, 7)
#rec_topic_choice = RecTagPicker(user_id)
#for i in xrange(10):
#    print rec_topic_choice.choice()

#key = REDIS_REC_USER_TAG%user_id
#redis.delete(key)
#print rec_read_more(user_id, 7)
#limit = 7
#offset = 0
#print rec_read_log_by_user_id_auto_more(10000000, limit, offset)
#print rec_read_by_user_id_tag_id(10184264, 10227250)
