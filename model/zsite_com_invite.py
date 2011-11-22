#coding:utf-8
from _db import Model
from model.zsite import Zsite, ZSITE_STATE_APPLY
from model.verify import verify_new
from model.zsite_member import zsite_member_new
from user_mail import mail_by_user_id

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

