#coding:utf-8
import _db
from model.zsite_list import zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, STATE_ADMIN , STATE_OWNER
from model.zsite import Zsite
from model.cid import CID_ZSITE_LIST_MEMBER 


ZSITE_MEMBER_STATE_OWNER = STATE_OWNER    # 创始人 
ZSITE_MEMBER_STATE_KERNEL = STATE_ADMIN   # 决策层
ZSITE_MEMBER_STATE_ACTIVE = STATE_ACTIVE  # 团队成员
ZSITE_MEMBER_STATE_LEAVE = STATE_DEL      # 已离职


def zsite_member_new(zsite_id, member_id, cid, state):
    pass

def zsite_member_rm(zsite_id, member_id):
    pass

def zsite_member_list(zsite_id, member_id, limit=None, offset=None):
    pass

def zsite_member_list_leave(zsite_id, member_id, limit=None, offset=None):
    pass

if __name__ == '__main__':
    pass

