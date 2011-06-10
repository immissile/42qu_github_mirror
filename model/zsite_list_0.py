#coding:utf-8
from zsite import Zsite
import zsite_list as zl

OWNER_ID = 0

def zsite_list(cid, limit=None, offset=None):
    return zl.zsite_list(0, cid, limit, offset)

def zsite_list_new(zsite_id, rank=1000):
    cid_list = [] # TODO
    zl.zsite_list_new(zsite_id, 0, cid_list, rank)

def zsite_list_rm(zsite_id):
    zl.zsite_list_rm(zsite_id, 0)

def zsite_list_get(zsite_id):
    zl.zsite_list_get(zsite_id, 0)

def zsite_list_rank(zsite_id, rank):
    zl.zsite_list_rank(zsite_id, 0, rank)
