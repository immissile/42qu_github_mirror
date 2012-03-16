import _env
from model.rec_read import *

def rec_read_po_rm_fix():
    from model.po import Po, STATE_ACTIVE


    for i in redis.keys(REDIS_REC_TAG_NEW%'*'):
        for j in redis.smembers(i):
            po = Po.mc_get(j)
            if po.state < STATE_ACTIVE:
                redis.srem(i, j)
                print po.link
                print i, j

    for i in redis.keys(REDIS_REC_TAG_OLD%'*'):
        for j in redis.zrange(i, 0, -1):
            po = Po.mc_get(j)
            if po.state < STATE_ACTIVE:
                print po.link
                redis.zrem(i, j)

    for i in redis.keys(REDIS_REC_USER_LOG%'*'):
        for j in redis.zrange(i, 0 , -1):
            po = Po.mc_get(j)
            if po.state < STATE_ACTIVE:
                print po.link
                redis.zrem(i, j)

    for i in redis.keys(REDIS_REC_USER_PO_TO_REC%('*','*')):
        print i
        redis.delete(i)
