#coding:utf-8
from config import SITE_HTTP
from model.mail import mq_rendermail
from model.zsite_list import zsite_list, zsite_list_new, STATE_RM, STATE_ACTIVE, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, STATE_ADMIN , STATE_OWNER, zsite_list_by_zsite_id_state, STATE_INVITE, zsite_id_list_order_id_desc, ZsiteList
from model.zsite import Zsite
from model.cid import CID_ZSITE_TUPLE_LIST_MEMBER, CID_VERIFY_MAIL
from model.po_review import po_review_state_set, po_review_list_active_by_zsite_id
from career import career_bind

ZSITE_MEMBER_STATE_OWNER = STATE_OWNER    # 创始人 
ZSITE_MEMBER_STATE_KERNEL = STATE_ADMIN   # 决策层
ZSITE_MEMBER_STATE_ACTIVE = STATE_ACTIVE  # 团队成员
ZSITE_MEMBER_STATE_INVITE = STATE_INVITE  # 已邀请
ZSITE_MEMBER_STATE_LEAVE = STATE_RM      # 已离职

def zsite_id_list_by_member_admin(id, limit=None, offset=None):
    return zsite_id_list_order_id_desc( id, CID_ZSITE_TUPLE_LIST_MEMBER, limit, offset)

def zsite_list_by_member_admin(id, limit=None, offset=None):
    return Zsite.mc_get_list(zsite_id_list_by_member_admin(id, limit, offset))

def zsite_id_count_by_member_admin(id):
    r = ZsiteList.where(zsite_id=id, cid=CID_ZSITE_TUPLE_LIST_MEMBER).where('state>=%s', STATE_ACTIVE)
    return r.count()

def zsite_member_new(
    zsite_id,
    member_id,
    state=ZSITE_MEMBER_STATE_INVITE
):
    id, _state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_TUPLE_LIST_MEMBER)
    if _state < state:
        zsite_list_new(zsite_id, member_id, CID_ZSITE_TUPLE_LIST_MEMBER, state=state)
        po_review_state_set(zsite_id, member_id, 1)
        return True

def zsite_member_admin_list(com_id):
    return Zsite.mc_get_list(zsite_id_list_by_zsite_id(com_id, CID_ZSITE_TUPLE_LIST_MEMBER))


def zsite_member_rm(zsite_id, member_id):
    zsite_list_rm(zsite_id, member_id, cid=CID_ZSITE_TUPLE_LIST_MEMBER)
    po_review_state_set(zsite_id, member_id, 0)

def zsite_member_list(zsite_id, state, limit=None, offset=None):
    return zsite_list_by_zsite_id_state(
        zsite_id, CID_ZSITE_TUPLE_LIST_MEMBER, state, limit, offset
    )


def zsite_member_invite_list(com_id):
    return zsite_member_list(com_id, ZSITE_MEMBER_STATE_INVITE)

def zsite_member_can_admin(zsite_id, member_id):
    id, state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_TUPLE_LIST_MEMBER)
    if id:
        return state >= ZSITE_MEMBER_STATE_ACTIVE

def zsite_member_is_invite(zsite_id, member_id):
    id, state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_TUPLE_LIST_MEMBER)
    return state == ZSITE_MEMBER_STATE_INVITE


def zsite_member_with_review(id):
    member_list = zsite_member_admin_list(id)
    review_list = po_review_list_active_by_zsite_id(id)
    review2member = dict((i.user_id, i) for i in review_list)

    career_bind(member_list)

    result_with_review = []
    result_without_review = []

    for i in member_list:
        mid = i.id

        if mid in review2member:
            review = review2member[mid]
            if not review.name_:
                review = None
        else:
            review = None

        i.review = review

        if review is None:
            result_without_review.append(i)
        else:
            result_with_review.append(i)


    result_with_review.extend(result_without_review)

    return result_with_review





if __name__ == '__main__':
    user = """
http://gongjun.42qu.com/
http://zhengtao.42qu.com/
http://shanfeng.42qu.com/
http://hijava.42qu.com/
http://10027580.42qu.com/
http://10020850.42qu.com/
"""
    zsite_id = 10186434 
    from zsite_url import id_by_url
    for i in user.split():
        url = i[7:i.find(".")]
        if url.isdigit():
            id = int(url)
        else:
            id = id_by_url(url)
        zsite_member_new(
            zsite_id,
            id,
            ZSITE_MEMBER_STATE_ACTIVE
        )
