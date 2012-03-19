#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite,   zsite_name_rm, ZSITE_STATE_ACTIVE 
from model.zsite_show import zsite_show_new, zsite_show_rm
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_ZSITE_TUPLE, CID_USER
from zkit.page import page_limit_offset
from model.zsite_verify import ZsiteUserVerifyed, ZSITE_USER_VERIFYED_CHECKED,ZSITE_USER_VERIFYED_UNCHECK
from model.pic import pic_no
from model.txt import txt_get, txt_new
from model.motto import motto as _motto
from model.user_mail import user_id_by_mail
from model.zsite_url import id_by_url
from model.user_session import user_session
from model.user_info import UserInfo
from model.zsite_rank import zsite_rank_max
from model.search_zsite import search_new
from config import SITE_DOMAIN, ADMIN_MAIL
from urlparse import urlparse
from model.zsite_url import id_by_url
from model.zsite import  zsite_by_query
from model.user_mail import user_id_by_mail
from model.spammer import spammer_new , spammer_rm
from model.career import career_rm

@urlmap('/zsite/(\d+)')
class Index(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        if zsite:
            info = UserInfo.get(id)
            if info:
                sex = info.sex
            else:
                sex = ''
            txt = txt_get(id)
            self.render(txt=txt, zsite=zsite, sex=sex)
        else:
            self.redirect('/')


    def post(self, id):
        zsite = Zsite.mc_get(id)
        user_info = UserInfo.get(id)

        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        txt = self.get_argument('txt', '')
        sex = self.get_argument('sex', 0)

        if name:
            zsite.name = name
            zsite.save()

        if motto:
            _motto.set(id, motto)

        if txt:
            txt_new(id, txt)

        if sex:
            user_info.sex = sex
            user_info.save()

        search_new(id)
        self.redirect('/zsite/%s' % id)


@urlmap('/zsite/pic/rm/(\d+)/(\d+)')
class PicRm(Base):
    def get(self, id, uid):
        admin_id = self.current_user.id
        pic_no(id, admin_id)
        self.redirect('/zsite/%s'%uid)

@urlmap('/zsite/name/rm/(\d+)')
class NameRm(Base):
    def get(self, id):
        zsite_name_rm(id)
        self.redirect('/zsite/%s'%id)

@urlmap('/zsite/show/(\d+)')
class Show(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        rank = self.get_argument('rank', 0)
        rank = int(rank)
        if zsite:
            zsite_show_new(id, zsite.cid, rank)
        self.redirect('/zsite/%s'%id)


@urlmap('/zsite/show/rm/(\d+)')
class ShowRm(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        zsite_show_rm(zsite)
        self.redirect('/zsite/%s'%id)


@urlmap('/zsite/mail/(\d+)')
class Mail(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        self.render(zsite=zsite)

    def post(self, id):
        zsite = Zsite.mc_get(id)
        title = self.get_argument('title', '')
        txt = self.get_argument('txt', '')
        if zsite and title and txt:
            mail = mail_by_user_id(id)
            name = zsite.name
            sendmail(title, txt, mail, name, ADMIN_MAIL)
        self.redirect('/zsite/%s' % id)


@urlmap('/zsite/verify/show/new/(\d+)')
class VerifyShowNew(Base):
    def get(self, id):
        zsite = Zsite.mc_get(id)
        zsite_show_new(id, zsite.cid)
        return self.redirect("/zsite/verify/next/%s"%id)


@urlmap('/zsite/verify/next/(\d+)')
class VerifyShowNext(Base):
    def get(self, id):
        zsite_user_verifyed = ZsiteUserVerifyed.get(
            user_id=id,
            state=ZSITE_USER_VERIFYED_UNCHECK
        )
        if zsite_user_verifyed:
            zsite_user_verifyed.state = ZSITE_USER_VERIFYED_CHECKED
            zsite_user_verifyed.save()
        return self.redirect("/zsite/verify/uncheck")

@urlmap('/zsite/verify/uncheck')
class VerifyUncheck(Base):
    def get(self):
        zsite_user_verifyed = ZsiteUserVerifyed.get(
            state=ZSITE_USER_VERIFYED_UNCHECK
        )
        if not zsite_user_verifyed:
            return self.redirect("/")
        zsite = Zsite.mc_get(zsite_user_verifyed.user_id)
        self.render(zsite=zsite)

    def post(self):
        id = self.get_argument('id')
        name = self.get_argument('name',None)
        pic = self.get_argument('pic',None)
        career_id_list = map(int,self.get_arguments('career',()))

        admin_id = self.current_user.id
        user = Zsite.mc_get(id)

        if career_id_list:
            for career_id in career_id_list:
                career_rm(career_id, int(id))
            from model.zsite_verify import zsite_verify_ajust
            zsite_verify_ajust(user)
        if name:
            zsite_name_rm(id)
        if pic:
            from model.ico import ico
            pic_no(ico.get(id), admin_id)
        return self.redirect("/zsite/verify/next/%s"%id)
        #return self.redirect("/zsite/verify/uncheck")

PAGE_LIMIT = 100




#def zsite_by_query(query):
#    user_id = None
#
#    if '@' in query:
#        user_id = user_id_by_mail(query)
#    elif SITE_DOMAIN in query:
#        key = urlparse(query).netloc.split('.', 1)[0]
#        user_id = id_by_url(key)
#    elif query.isdigit():
#        if Zsite.mc_get(query):
#            user_id = query
#    else:
#        query = query.replace('http://', '')
#        user_id = id_by_url(query)
#
#    return user_id


@urlmap('/zsite/user_search')
class UserSearch(Base):
    def get(self):
        self.render(
            input='',
        )

    def post(self):
        query = self.get_argument('input', None)
        if query:

            user_id = zsite_by_query(query)
            if user_id:
                url = '/zsite/%s' % user_id
                return self.redirect(url)
            else:
                self.render(input=query)
        else:
            self.get()


@urlmap('/sudo/(\d+)')
class Sudo(Base):
    def get(self, avatar_id):
        session = user_session(avatar_id)
        self.set_cookie('S', session)
        next = self.get_argument('next', None)
        current_user = Zsite.mc_get(avatar_id)
        if next:
            self.redirect(next)
        else:
            self.redirect(current_user.link)


@urlmap('/test_account')
class TestAccount(Base):
    def get(self):
        self.render()

@urlmap('/zsite/spammer/rm/(\d+)')
class SpammerRm(Base):
    def get(self,id):
        spammer_rm(id)
        self.redirect('/zsite/%s' % id)

@urlmap('/zsite/spammer/new/(\d+)')
class SpammerNew(Base):
    def get(self,id):
        spammer_new(id)
        self.redirect('/zsite/%s' % id)
