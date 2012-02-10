#coding:utf-8
from _db import McCache
from time import time
from model.po_json import po_json
from model.days import time_new_offset
from zkit.algorithm.wrandom import wsample2

REDIS_REC_LOG = 'Rec:%s'

def rec_read_by_topic(topic_id):
    return 

def topic_id_by_user_id(user_id):
    user_topic = [] 

    if user_topic:
        user_topic_picker = wsample2(user_topic)
    

def rec_read(user_id, limit):
    now = time_new_offset()

    if limit < 0:
        limit = 0

    t = []
    count = 0
    offset = 0

    while count < limit:
        topic_id = user_topic_picker()[0]
        if not topic_id:
            continue
        i = rec_read_by_topic(topic_id)
        t.append(i)
        t.append(now+offset)

        offset += 0.01
        count += 1

    if count:
        key_log = REDIS_REC_LOG%user_id
        redis.zadd(key_log, *t)

def rec_read_log_by_user_id(user_id, limit, offset):
    key = REDIS_REC_LOG%user_id
    return  redis.zrevrange(key, offset, offset+limit-1)


def rec_read_more(user_id, limit):
    if rec_read(user_id, limit):
        return rec_read_log_by_user_id(user_id, limit)
    return []

def po_json_by_rec_read(user_id, limit=8):
    id_list = rec_read_more(user_id, limit)
    return po_json(user_id , id_list, 47)

if __name__ == '__main__':
    pass
    

    user_id = 10000000
    #print rec_read_page(user_id, limit=7, offset=0)
    #print rec_read_count(user_id)

    #from model.po import Po,STATE_ACTIVE
    #for cid in REDIS_REC_CID_DICT:
    #    id_list = redis.zrevrange(REDIS_REC_CID%cid, 0, -1 )
    #    for po in Po.mc_get_list(id_list):
    #        po.state = STATE_ACTIVE
    #        po.save()

    #from model.po import Po
    #mc_rec_lock.delete(user_id)
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
