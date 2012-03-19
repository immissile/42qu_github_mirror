#coding:utf-8

from _db import cursor_by_table, McModel, McCache, McNum, Model, McCacheM, McCacheA
from model.zsite import Zsite
from kv import Kv

TopRec = Kv('top_rec', 0)

TOP_REC_CID = 0b11111111111111111111111111111111
TOP_REC_CID_OAUTH_BINDED = 0b00000000000000000000000000000001
TOP_REC_CID_SITE_REC = 0b00000000000000000000000000000010

def top_rec(user_id):
    return TopRec.get(user_id)

def top_rec_mark(user_id, cid):
    old = top_rec(user_id)
    old|=cid
    TopRec.set(user_id, old)
    return old

def top_rec_unmark(user_id, cid):
    old = top_rec(user_id)
    old&=(TOP_REC_CID^cid)
    TopRec.set(user_id, old)
    return old

if __name__ == '__main__':
    print top_rec_mark(10008640, TOP_REC_CID_SITE_REC)


