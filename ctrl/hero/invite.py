# -*- coding: utf-8 -*-
from _handler import Base, LoginBase
from ctrl._urlmap.hero import urlmap
from model.follow import follow_id_list_by_from_id
from model.invite_email import invite_user_id_list_by_cid, CID_MSN, CID_QQ, invite_invite_email_list_by_cid, invite_message_new

@urlmap('/invite')
class Invite(LoginBase):
    def get(self):
        self.render()


@urlmap('/invite/login/(\d+)')
class InviteLogin(LoginBase):
    def get(self, cid=CID_MSN):
        if cid != CID_QQ:
            self.render(cid=cid)
        else:
            self.render('/ctrl/me/i/import_qq.htm')

@urlmap('/invite/show')
@urlmap('/invite/show/(\d+)')
class InviteShow(LoginBase):
    def get(self, cid=CID_MSN):
        uid = self.current_user_id
        user_id_list = invite_user_id_list_by_cid(uid, cid)
        follow_id_list = follow_id_list_by_from_id(uid)
        user_id_list = set(user_id_list) - set(follow_id_list)
        if not user_id_list:
            return self.redirect('/invite/email/%s'%cid)
        self.render(cid=cid, user_id_list=user_id_list)

    def post(self, cid=CID_MSN):
        user_id = self.current_user_id
        fid_list = self.get_argument('follow_id_list', None)
        if fid_list:
            fid_list = fid_list.split(' ')
            for i in Zsite.mc_get_list(fid_list):
                if i.id != user_id:
                    follow_new(user_id, i.id)

        self.redirect('/invite/email/%s'%cid)

@urlmap('/invite/email')
@urlmap('/invite/email/(\d+)')
class InviteEmail(LoginBase):
    def get(self, cid=CID_MSN):
        emails = invite_invite_email_list_by_cid(self.current_user_id, cid)
        if not emails:
            return self.render('ctrl/hero/invite/invite.htm', success=True)

        self.render(emails=emails, cid=cid)

    def post(self, cid=CID_MSN):
        emails = self.get_arguments('mails', None)
        mail_txt = self.get_argument('mail_txt', None)
        if emails:
            invite_message_new(self.current_user_id, emails, mail_txt)
        self.render('ctrl/hero/invite/invite.htm', success=True)
