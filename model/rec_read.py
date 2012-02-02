#coding:utf-8
from _db import redis , McCache
from zkit.zitertools import lineiter
from zkit.algorithm.wrandom import limit_by_rank
from time import time
from random import shuffle
from array import array
from model.po_json import po_json

REDIS_REC_CID_TUPLE = (
    (1, '女性·时尚·星座'),
    (2, '网络·科技·创业'),
    (3, '情感·社会·心理'),
    (4, '图书·电影·音乐'),
    (5, '职业·成长·学习'),
    (6, '政治·经济·历史'),
    (7, '生活·旅行·健康'),
    (8, '文学·艺术·诗歌'),
    (9, '酷知识'),
)

REDIS_REC_CID_DICT = dict(REDIS_REC_CID_TUPLE)
REDIS_REC_CID_LEN = len(REDIS_REC_CID_TUPLE)
REDIS_REC_CID = 'RecCid:%s'
REDIS_REC_CID_POS = 'RecCid#%s'
REDIS_REC_READ = 'RecRead:%s'
REDIS_REC_LOG = 'RecLog:%s'
REDIS_REC_RANK = 'RecRank:%s'
mc_rec_lock = McCache('RecLock:%s')

def time_now():
    return int(time() - 1327823396)

def rec_read(user_id, limit=7):
    key = REDIS_REC_READ%user_id

    now = time_now()

    if limit < 0:
        limit = 0

    total = 0
    key_log = REDIS_REC_LOG%user_id

    t = []


    offset = 0
    count = 0

    while True:
        result = redis.zrevrange(key , total, total+limit-1, False)


        for i in result:
            total += 1

            if redis.zscore(key_log, i):
                continue

            t.append(i)
            t.append(now+offset)
            offset -= 0.1
            count += 1

            if count >= limit:
                break

        if count >= limit or len(result) < limit:
            break


    if total:
        redis.zremrangebyrank(key, -total , -1)

    diff = limit - count

    while diff > 0:
        result = rec_read_cid(user_id, limit)
        if not result:
            break

        for i in result:
            if redis.zscore(key_log, i):
                continue

            t.append(i)
            t.append(now+offset)
            offset -= 0.1
            count += 1

            if count >= limit:
                break

        diff = limit - count

    if t:
        redis.zadd(key_log, *t)

    return t


def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))

REC_READ_LOCK_MIN = 3

def rec_read_more(user_id, limit):
    lock = mc_rec_lock.get(user_id) or 0

    if lock < REC_READ_LOCK_MIN :
        result = rec_read(user_id, limit)

        if result:
            lock = lock+1
            timeout = 300
        else:
            lock = REC_READ_LOCK_MIN+1
            timeout = 3600

        mc_rec_lock.set(user_id, lock, timeout)

        return result

    return ()


def rec_read_lastest(user_id, limit=7):
    if rec_read_more(user_id, limit):
        return rec_read_by_user_id(user_id, limit)
    return ()

def rec_read_page(user_id, limit=7, offset=0):
    if offset == 0:
        rec_read_more(user_id, limit)
    return rec_read_by_user_id(user_id, limit, offset)


def rec_read_by_user_id(user_id, limit, offset=0):
    key = REDIS_REC_LOG%user_id
    return  redis.zrevrange(key, offset, offset+limit-1)

def rec_read_lastest_with_len(user_id, limit=7, offset=0):
    return redis.zcard(key), rec_read_lastest(user_id, limit, offset)

from model.po import Po


def po_by_rec_read_equal_limit(user_id, limit=7):
    key = REDIS_REC_READ%user_id
    if redis.zcard(key) < limit:
        return []
    return po_by_rec_read(user_id)

def rec_read_empty(user_id):
    for key in (
        REDIS_REC_CID_POS,
        REDIS_REC_READ,
        REDIS_REC_LOG,
        REDIS_REC_RANK
    ):
        redis.delete(key%user_id)

    mc_rec_lock.delete(user_id)

#rec cid

def rec_cid_push(cid, id):
    return redis.zadd(REDIS_REC_CID%cid, id, time_now())

#def rec_cid_extend(cid, id_time_list):
#    cid = int(cid)
#
#    if cid not in REDIS_REC_CID_DICT:
#        return
#
#    return redis.zadd(REDIS_REC_CID%cid, *lineiter(id_time_list))

REC_USER_CID_RANK_DEFAULT_FOR_MAN = [0.25/REDIS_REC_CID_LEN]
REC_USER_CID_RANK_DEFAULT_FOR_WOMAN = [2.0/REDIS_REC_CID_LEN]
REC_USER_CID_RANK_DEFAULT_FOR_0 = [1.0/REDIS_REC_CID_LEN]

def redis_rec_cid_rank_default(rank):
    total = REDIS_REC_CID_LEN - 1
    begin = rank[0]
    base = (1-begin)/total
    rank.extend([
        i*base+begin
        for i in xrange(1, total)
    ])
    r = array('f')
    r.fromlist(rank)
    return r

REC_USER_CID_RANK_DEFAULT = map(redis_rec_cid_rank_default, (
    REC_USER_CID_RANK_DEFAULT_FOR_0,
    REC_USER_CID_RANK_DEFAULT_FOR_MAN,
    REC_USER_CID_RANK_DEFAULT_FOR_WOMAN
))

def rec_user_cid_rank(user_id):
    from model.user_info import user_sex
    key = REDIS_REC_RANK%user_id
    rank = redis.get(key)

    if not rank:
        rank = REC_USER_CID_RANK_DEFAULT[user_sex(user_id)]
        redis.set(key, rank.tostring())
    else:
        t = array('f')
        t.fromstring(rank)
        rank = t

    return rank

def rec_user_cid_limit(user_id, limit):
    return limit_by_rank(rec_user_cid_rank(user_id), limit)

def rec_cid_pos_by_user_id(user_id):
    key = REDIS_REC_CID_POS%user_id
    result = redis.lrange(key, 0, -1)
    diff = REDIS_REC_CID_LEN - len(result)
    if diff:
        more = [0]*diff
        result.extend(more)
        redis.rpush(key, *more)
    return result

def rec_read_cid(user_id, limit):
    result = []
    rec_pos_update = []
    can_rec_cid = set(REDIS_REC_CID_DICT)
    cid_range = range(1, REDIS_REC_CID_LEN+1)

    def _(cid, start, cid_limit):
        r = redis.zrangebyscore(REDIS_REC_CID%cid, '(%s'%start, '+inf', 0, cid_limit, True)
        if r:
            last = r[-1][1]
            result.extend([i[0] for i in r])
        else:
            last = start
            can_rec_cid.remove(cid)

        return last


    for cid, start, cid_limit in zip(
        cid_range,
        rec_cid_pos_by_user_id(user_id),
        rec_user_cid_limit(user_id, limit)
    ):
        if cid_limit:
            last = _(cid, start, cid_limit)
        else:
            last = start
        rec_pos_update.append(last)

    rec_pos_dict = None

    while True:
        diff = limit - len(result)

        if diff <= 0 or not can_rec_cid:
            break

        cid_limit = int(1+(diff / len(can_rec_cid)))

        if rec_pos_dict is None:
            rec_pos_dict = dict(zip(cid_range, rec_pos_update))


        cid_list = list(can_rec_cid)
        shuffle(cid_list)
        for cid in cid_list:
            start = rec_pos_dict[cid]
            diff = limit - len(result)
            if diff <= 0:
                break
            elif cid_limit > diff:
                cid_limit = diff
            rec_pos_dict[cid] = _(cid, start, cid_limit)

    if rec_pos_dict is not None:
        rec_pos_update = [rec_pos_dict[i] for i in cid_range]

    if result:
        key = REDIS_REC_CID_POS%user_id

        p = redis.pipeline()
        p.delete(key)
        p.rpush(key, *rec_pos_update)
        p.execute()

    shuffle( result )
    return result

def rec_id_by_cid(cid, limit=-1, offset=0):
    if limit != -1:
        limit = offset+limit-1
    return redis.zrevrange(REDIS_REC_CID%cid, offset, limit )

def rec_cid_mv(po_id, old_cid, new_cid):
    rec_rm(po_id, old_cid)
    rec_cid_push(new_cid, po_id)

def rec_rm(po_id, cid):
    redis.zrem(REDIS_REC_CID%cid, po_id)

def po_json_by_rec_read(user_id, limit=8):
    id_list = rec_read_lastest(user_id, limit)
    return po_json(user_id , id_list, 47)

def rec_cid_count(cid):
    return redis.zcount(REDIS_REC_CID%cid, '-inf', '+inf')

if __name__ == '__main__':
    #from model.po import Po,STATE_ACTIVE
    #for cid in REDIS_REC_CID_DICT:
    #    id_list = redis.zrevrange(REDIS_REC_CID%cid, 0, -1 )
    #    for po in Po.mc_get_list(id_list):
    #        po.state = STATE_ACTIVE
    #        po.save()

    user_id = 10000000
    from model.po import Po
    mc_rec_lock.delete(user_id)
    #rec_read_empty(user_id)

    #rec_cid_push(2, 3)
    #print redis.zrange(REDIS_REC_CID%1, 0, 11)
    #print rec_read_more(user_id,7)
    #print redis.zrange(REDIS_REC_CID%1, 0, 11)
    #print 'old',rec_id_by_cid(1,11)
    ##rec_cid_mv(69202,1,2)
    #print 'new',rec_id_by_cid(1)
    #print 'new2',rec_id_by_cid(2,11)
    #print rec_cid_count(1)

    #   rec_read_extend(user_id, [(1, 1), (2, 2)])
#    print rec_read_lastest(user_id,1)
    #print rec_cid_pos_by_user_id(user_id)
    #rec_cid_pos_update(user_id, ((1, 1), ))
    #cid = 1
    #test = list(zip(range(100), range(100)))
#    rec_cid_extend(1, test)
#    print redis.zrangebyscore(REDIS_REC_CID%cid, "(3", '+inf', 0,7)
    #result = rec_read_lastest(user_id, 7, 0)
    #print result , len(result)

    #for i in REDIS_REC_CID_DICT:
    #    redis.delete(REDIS_REC_CID%i)
#    print len(REC_USER_CID_RANK_DEFAULT)
#    print REC_USER_CID_RANK_DEFAULT
#    print type(REC_USER_CID_RANK_DEFAULT[0])
    #print rec_read_empty(user_id)
    #print po_json_by_rec_read(user_id)
    #print rec_read_empty(10001518)
    #print rec_read_cid(user_id, 3)
    #print redis.zrangebyscore(REDIS_REC_CID%1, 68603, 99999999, 0, 33, True)
    #print rec_user_cid_rank(user_id)
