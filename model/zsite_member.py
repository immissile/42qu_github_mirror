#coding:utf-8
from _db import Model
from config import SITE_HTTP
from model.mail import mq_rendermail, rendermail
from model.zsite_list import zsite_list, zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, STATE_ADMIN , STATE_OWNER, zsite_list_by_zsite_id_state,STATE_INVITE, zsite_id_list_order_id_desc, ZsiteList
from model.zsite import Zsite, ZSITE_STATE_APPLY
from model.cid import CID_ZSITE_LIST_MEMBER, CID_VERIFY_MAIL, CID_USER
from model.verify import verify_new
from user_mail import mail_by_user_id
from model.po_review import po_review_state_set, po_review_list_active_by_zsite_id
from career import career_bind

ZSITE_MEMBER_STATE_OWNER = STATE_OWNER    # 创始人 
ZSITE_MEMBER_STATE_KERNEL = STATE_ADMIN   # 决策层
ZSITE_MEMBER_STATE_ACTIVE = STATE_ACTIVE  # 团队成员
ZSITE_MEMBER_STATE_INVITE = STATE_INVITE  # 已邀请
ZSITE_MEMBER_STATE_LEAVE = STATE_DEL      # 已离职

def zsite_id_list_by_member_admin(id, limit=None, offset=None):
    return zsite_id_list_order_id_desc( id, CID_ZSITE_LIST_MEMBER, limit, offset)

def zsite_list_by_member_admin(id, limit=None, offset=None):
    return Zsite.mc_get_list(zsite_id_list_by_member_admin(id, limit, offset))

def zsite_id_count_by_member_admin(id):
    r =  ZsiteList.where(zsite_id=id,cid=CID_ZSITE_LIST_MEMBER).where('state>=%s',STATE_ACTIVE)
    return r.count()

def zsite_member_new(
    zsite_id, 
    member_id,  
    state=ZSITE_MEMBER_STATE_INVITE, 
    cid=CID_ZSITE_LIST_MEMBER
):
    id, _state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_LIST_MEMBER)
    if _state < state:
        zsite_list_new(zsite_id, member_id, CID_ZSITE_LIST_MEMBER, state=state)
        po_review_state_set(zsite_id, member_id, 1)
        return True

def zsite_member_admin_list(com_id):
    return Zsite.mc_get_list(zsite_id_list_by_zsite_id(com_id,CID_ZSITE_LIST_MEMBER))


def zsite_member_rm(zsite_id, member_id):
    zsite_list_rm(zsite_id, member_id, cid=CID_ZSITE_LIST_MEMBER)
    po_review_state_set(zsite_id, member_id, 0)

def zsite_member_list(zsite_id, state, limit=None, offset=None):
    return zsite_list_by_zsite_id_state(
        zsite_id, CID_ZSITE_LIST_MEMBER, state, limit, offset
    )

    
def zsite_member_invite_list(com_id):
    return zsite_member_list(com_id,ZSITE_MEMBER_STATE_INVITE)

def zsite_member_can_admin(zsite_id, member_id):
    id, state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_LIST_MEMBER)
    if id:
        return state >= ZSITE_MEMBER_STATE_INVITE

def zsite_member_invite(
    zsite, member_id_list, current_user
):
    if type(member_id_list) in (str, int, long):
        member_id_list = [member_id_list,]
    
    member_id_list = map(int,member_id_list)

    follower_list = [
        i for i in
        Zsite.mc_get_list(member_id_list)
        if i and i.cid == CID_USER
    ]

    for i in follower_list:
        _zsite_member_invite(zsite, i, current_user)

def _zsite_member_invite(zsite, member, current_user):
    zsite_id = zsite.id
    member_id =  member.id

    if member.state <= ZSITE_STATE_APPLY:
        verify_id, verify_value = verify_new(member_id, CID_VERIFY_MAIL)
        http = "%s/auth/verify/mail/%s/%s?next="%(
            SITE_HTTP,
            verify_id, 
            verify_value
        )
    else:
        http = "http:"

    if zsite_member_new(zsite_id, member_id):
        #TODO !
        mail = mail_by_user_id(member_id)
        mail = "zsp007@gmail.com"

        rendermail(
            '/mail/com/invite_member.htm', 
            mail, 
            member.name,
            sender_name = current_user.name,
            format='html',
            subject='%s 邀请您给 %s 未来的同事写几句话' % (
                current_user.name, 
                zsite.name
            ),
            from_user_name = current_user.name,
            from_user_link = current_user.link,
            com_link = zsite.link,
            com_name = zsite.name,
            http = http 
        )



def zsite_member_with_review(id):
    member_list = zsite_member_admin_list(id)
    review_list = po_review_list_active_by_zsite_id(id)
    review2member = dict((i.user_id,i) for i in review_list)

    career_bind(member_list)
 
    result_with_review = []
    result_without_review = []
       
    for i in member_list:
        mid = i.id
        if mid in review2member:
            i.review = review2member[mid]
            result_with_review.append(i)
        else:
            i.review = None
            result_without_review.append(i)
            
    result_with_review.extend(result_without_review)

    return result_with_review





if __name__ == '__main__':
    zsite_id = 895
    for i in zsite_member_with_review(zsite_id):
        review = i.review
        print i.name
        if review:
            print "\t",review.name


