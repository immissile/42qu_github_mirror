#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from ctrl._util.search import search_get
from model.search import search_user
from model.zsite import Zsite
from model.cid import CID_USER
from zkit.txt import EMAIL_VALID
from model.user_mail import user_id_by_mail
from model.user_auth import user_new_by_mail
from zkit.errtip import Errtip
from model.com_apply import com_apply_new, com_apply_get, com_apply_rm, com_apply_accept
from model.zsite_member import zsite_member_rm, zsite_member_invite, zsite_member_new, ZSITE_MEMBER_STATE_ACTIVE, zsite_id_count_by_member_admin
from zkit.txt import EMAIL_VALID
from model.zsite_url import id_by_url

#@urlmap('/member/new/result')
#class MemberNewResult(AdminBase):
#    def get(self):
#        return self.render()

@urlmap('/member/new/search')
class MemberNewSearch(AdminBase):
    search = staticmethod(search_user)
    link = '/member/new/search-%%s?q=%s'
    PAGE_LIMIT = 1024
    get = search_get

    def post(self):
        zsite_id = self.zsite_id

        follow_id_list = self.get_argument('follow_id_list', None)
        if follow_id_list:
            zsite_member_invite(
                self.zsite,
                follow_id_list.split(),
                self.current_user
            )

        return self.redirect(self.request.path)

@urlmap('/member/apply/(\d+)/(\d+)')
class MemberApply(AdminBase):
    def get(self,state,id):
        if state.isdigit and id.isdigit:
            state = int(state)
            com_id = self.zsite_id
            id = int(id)
            if state:
                zsite_member_new(com_id,id,ZSITE_MEMBER_STATE_ACTIVE)
                com_apply_accept(id,com_id,self.current_user_id)
            else:
                com_apply_rm(id,com_id,self.current_user_id)
        self.redirect('/member/admin')

@urlmap('/member/invite/rm')
class MemberInvite(AdminBase):
    def post(self):
        id = self.get_argument('id',None)
        if id and zsite_id_count_by_member_admin(com_id)>1:
            zsite_member_rm(self.zsite_id,id)
        self.redirect('/member/admin')

@urlmap('/member/rm')
class MemberRm(AdminBase):
    def post(self):
        id = self.get_argument('id',None)
        print zsite_id_count_by_member_admin(com_id)
        com_id = self.zsite_id
        if id and zsite_id_count_by_member_admin(com_id)>1:
            print zsite_id_count_by_member_admin(com_id)
            zsite_member_rm(com_id,id)
        self.finish(True)

@urlmap('/member/admin')
class MemberAdmin(AdminBase):
    def get(self):
        self.render(com_id=self.zsite_id)

@urlmap('/member/join')
class MemberJoin(ZsiteBase):
    def get(self):
        user_id = self.current_user_id
        com_id = self.zsite_id
        if com_apply_get(user_id,com_id):
            zsite_member_new(com_id,user_id,ZSITE_MEMBER_STATE_ACTIVE)
        else:
            com_apply_new(user_id,com_id)
        self.redirect('/')



@urlmap('/member/admin/invite')
class MemberAdminInvite(AdminBase):
    def get(self):
        self.render()

    def post(self):
        print self.request.arguments,'!!!'
        links = self.get_arguments('link',None)
        links = filter(lambda x:x.lstrip('http://').split('.')[0],links)
        uids = filter(lambda x:id_by_url(x),links)
        emails = self.get_arguments('email',None)
        names = self.get_arguments('name',None)
        invite_address =  zip(emails,names)
        com = self.zsite
        current_user = self.current_user
        
        
        for n,(i,j) in invite_address:
            if i or j:
                del invite_address[n]
            if not EMAIL_VALID.match(i):
                del invite_address[n]
        if uids:
            for uesr_id in uids:
                zsite_member_invite(com, user_id, current_user)



        if invite_address:
            for mail,name in invite_address:
                user_id = user_id_by_mail(mail)
                if not user_id:
                    user = user_new_by_mail(mail, name=name)
                    user_id = user.id

                zsite_member_invite(self.zsite, user_id, self.current_user)

        self.render(success=True)


@urlmap('/member/new/invite')
class MemberNewInvite(AdminBase):
    def get(self):
        return self.render()

    def post(self):
        arguments = self.request.arguments
        for mail, name in zip(arguments['mail'], arguments['name']):
            mail = mail.strip().lower()
            name = name.strip()
            if EMAIL_VALID.match(mail):
                user_id = user_id_by_mail(mail)
                if not user_id:
                    user = user_new_by_mail(mail, name=name)
                    user_id = user.id

                zsite_member_invite(self.zsite, user_id, self.current_user)

        return self.redirect('/review/invite')

@urlmap('/review/invite')
class ReviewInvite(AdminBase):
    def get(self):
        return self.render()

@urlmap('/member/new/reg')
class MemberNewReg(AdminBase):
    def get(self):
        id_list = SHOW_LIST
        zsite_list = filter(bool, Zsite.mc_get_list(id_list))
        self.render(
            sex=0,
            password='',
            errtip=Errtip(),
            zsite_list=zsite_list,
        )


