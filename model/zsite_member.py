#coding:utf-8
from _db import Model

from model.zsite_list import zsite_list, zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, STATE_ADMIN , STATE_OWNER, zsite_list_by_zsite_id_state
from model.zsite import Zsite
from model.cid import CID_ZSITE_LIST_MEMBER, CID_VERIFY_COM_MEMBER
from model.verify import verify_new

ZSITE_MEMBER_STATE_OWNER = STATE_OWNER    # 创始人 
ZSITE_MEMBER_STATE_KERNEL = STATE_ADMIN   # 决策层
ZSITE_MEMBER_STATE_ACTIVE = STATE_ACTIVE  # 团队成员
ZSITE_MEMBER_STATE_LEAVE = STATE_DEL      # 已离职

class ZsiteMemberInvite(Model):
    pass



def zsite_member_new(zsite_id, member_id, cid=CID_ZSITE_LIST_MEMBER, state=ZSITE_MEMBER_STATE_ACTIVE):
    zsite_list_new(zsite_id, member_id, CID_ZSITE_LIST_MEMBER, state=state)

def zsite_member_rm(zsite_id, member_id):
    zsite_list_rm(zsite_id, member_id, cid=CID_ZSITE_LIST_MEMBER)

def zsite_member_list(zsite_id, member_id, state, limit=None, offset=None):
    return zsite_list_by_zsite_id_state(zsite_id, member_id, state, limit, offset)

def zsite_member_can_admin(zsite_id, member_id):
    id, state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_LIST_MEMBER)
    if id:
        return state >= ZSITE_MEMBER_STATE_ACTIVE

def zsite_member_invite(zsite_id, member_id):
    return zsite_member_invite_email_name_unit_title(zsite_id, name, '', '')

def zsite_member_invite_email_name_unit_title(zsite_id, name, unit, title):
    id, value = verify_new(member_id, CID_VERIFY_COM_MEMBER)
    invite = ZsiteMemberInvite(
        id=id,
        zsite_id=zsite_id,
        unit=unit,
        title=title
    )
    invite.save()
    return id, value 

if __name__ == '__main__':
    pass

