import _env
from model.rec_read import *
from model.po_tag import _tag_rm_by_user_id_list, REDIS_TAG_CID
from model.po import Po, STATE_ACTIVE

def rec_read_po_rm_fix():
    for i in  redis.keys(REDIS_TAG_CID%('*','*')):
        tag_id = i[7:15]
        cid = int(i.split(":")[-1])
        for j in redis.zrange(i, 0, -1):
            po = Po.mc_get(j)
            if po.state < STATE_ACTIVE:
                _tag_rm_by_user_id_list(po, po.user_id, [tag_id])
                print "po_tag_rm_by_po(po)",tag_id, j


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


rec_read_po_rm_fix()
