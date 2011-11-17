#coding:utf-8
from _db import Model
from model.mail import mq_rendermail
from model.zsite_list import zsite_list, zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id, STATE_ADMIN , STATE_OWNER, zsite_list_by_zsite_id_state,STATE_INVITE
from model.zsite import Zsite
from model.cid import CID_ZSITE_LIST_MEMBER, CID_VERIFY_COM_MEMBER
from model.verify import verify_new
from user_mail import mail_by_user_id

ZSITE_MEMBER_STATE_OWNER = STATE_OWNER    # 创始人 
ZSITE_MEMBER_STATE_KERNEL = STATE_ADMIN   # 决策层
ZSITE_MEMBER_STATE_ACTIVE = STATE_ACTIVE  # 团队成员
ZSITE_MEMBER_STATE_INVITE = STATE_INVITE  # 已邀请
ZSITE_MEMBER_STATE_LEAVE = STATE_DEL      # 已离职

class ZsiteMemberInvite(Model):
    pass



def zsite_member_new(zsite_id, member_id, cid=CID_ZSITE_LIST_MEMBER, state=ZSITE_MEMBER_STATE_INVITE):
    id, _state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_LIST_MEMBER)
    if _state < state:
        zsite_list_new(zsite_id, member_id, CID_ZSITE_LIST_MEMBER, state=state)
        return True


def zsite_member_rm(zsite_id, member_id):
    zsite_list_rm(zsite_id, member_id, cid=CID_ZSITE_LIST_MEMBER)

def zsite_member_list(zsite_id, state, limit=None, offset=None):
    return zsite_list_by_zsite_id_state(
        zsite_id, CID_ZSITE_LIST_MEMBER, state, limit, offset
    )

def zsite_member_can_admin(zsite_id, member_id):
    id, state = zsite_list_id_state(zsite_id, member_id, CID_ZSITE_LIST_MEMBER)
    if id:
        return state >= ZSITE_MEMBER_STATE_ACTIVE

def zsite_member_invite(
    zsite, member_id_list, current_user
):
    if type(member_id_list) in (str, int):
        member_id_list = [member_id_list,]

    follower_list = [
        i for i in
        Zsite.mc_get_list(follow_id_list)
        if i and i.cid == CID_USER
    ]
    member_id_list = map(int,member_id_list)

    for i in member_id_list:
        _zsite_member_invite(zsite, i, current_user)

def _zsite_member_invite(zsite, member, current_user):
    zsite_id = zsite.id
    member_id =  member.id

    if zsite_member_new(zsite_id, member_id):
        mail = mail_by_user_id(member_id)
        mail = "zsp007@gmail.com"

        mq_rendermail(
            '/mail/com/invite_member.htm', 
            mail, 
            member.name,
            sender_name = current_user.name,
            format='html',
            subject='%s 邀请您给 %s 未来的同事写几句话' % (
                current_user.name, 
                zsite.name
            ),
            from_user=from_user,
            com = zsite
        )

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

