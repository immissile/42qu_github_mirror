#coding:utf-8
from _db import Model
from model.zsite import Zsite, ZSITE_STATE_APPLY
from model.verify import verify_new
from model.zsite_member import zsite_member_new
from user_mail import mail_by_user_id
from config import SITE_HTTP
from model.career import career_current
from model.cid import CID_USER, CID_VERIFY_MAIL
from model.mail import mq_rendermail, rendermail

def member_list_by_id_list(member_id_list):
    if type(member_id_list) in (str, int, long):
        member_id_list = [member_id_list, ]

    member_id_list = map(int, member_id_list)

    follower_list = [
        i for i in
        Zsite.mc_get_list(member_id_list)
        if i and i.cid == CID_USER
    ]
    return follower_list

def http_by_member(member):
    member_id = member.id
    if member.state <= ZSITE_STATE_APPLY:
        verify_id, verify_value = verify_new(member_id, CID_VERIFY_MAIL)
        http = '%s/auth/verify/mail/%s/%s?next='%(
            SITE_HTTP,
            verify_id,
            verify_value
        )
    else:
        http = 'http:'
    return http

def zsite_member_invite( zsite, member_id_list, current_user):

    for i in member_list_by_id_list(member_id_list):
        _zsite_member_invite(zsite, i, current_user)

def _zsite_member_invite(zsite, member, current_user):
    zsite_id = zsite.id
    member_id = member.id

    http = http_by_member(member)

    if zsite_member_new(zsite_id, member_id):
        #TODO !
        mail = mail_by_user_id(member_id)
        #mail = "zsp007@gmail.com"

        mq_rendermail(
            '/mail/com/invite_member.htm',
            mail,
            member.name,
            sender_name=current_user.name,
            format='html',
            subject='%s 邀请您给 %s 未来的同事写几句话' % (
                current_user.name,
                zsite.name
            ),
            from_user_name=current_user.name,
            from_user_link=current_user.link,
            com_link=zsite.link,
            com_name=zsite.name,
            http=http
        )

def zsite_review_invite(zsite, member_id_list, current_user):
    for i in member_list_by_id_list(member_id_list):
        _zsite_review_invite(zsite, i, current_user)

def _zsite_review_invite(zsite, member, current_user):
    zsite_id = zsite.id
    member_id = member.id

    http = http_by_member(member)

    #TODO !
    mail = mail_by_user_id(member_id)
#    mail = "zsp007@gmail.com"

    name = [current_user.name]
    name.extend( career_current(current_user.id) )
    name = ' , '.join(filter(bool, name))

    mq_rendermail(
        '/mail/com/invite_review.htm',
        mail,
        member.name,
        sender_name=current_user.name,
        format='html',
        subject='%s 邀请您给 %s 写推荐语' % (
            name,
            zsite.name
        ),
        from_user_name=name,
        from_user_link=current_user.link,
        com_link=zsite.link,
        com_name=zsite.name,
        http=http
    )




