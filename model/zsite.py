#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import escape
from cid import CID_USER, CID_SITE
from _db import Model, McModel
from gid import gid
from txt import txt_property
from zkit.attrcache import attrcache

ZSITE_STATE_BAN = 1
ZSITE_STATE_NO_MAIL = 5
ZSITE_STATE_NO_PASSWORD = 6
ZSITE_STATE_APPLY = 10
ZSITE_STATE_ACTIVE = 15
ZSITE_STATE_FAILED_VERIFY = 20
ZSITE_STATE_WAIT_VERIFY = 25
ZSITE_STATE_VERIFY_CANNOT_REPLY = 30
ZSITE_STATE_CAN_REPLY = 35
ZSITE_STATE_VERIFY = 40

#ZPAGE_NAME = "主页"
#
#ZPAGE_STATE_INDEX = 10


class Zsite(McModel):
    txt = txt_property

    @attrcache
    def link(self):
        from zsite_url import link
        return link(self.id)

    @attrcache
    def link_html(self):
        return '<a href="%s">%s</a>' % (self.link, escape(self.name))

    @attrcache
    def _ico96(self):
        from ico import ico_url
        return ico_url(self.id)

    @property
    def ico96(self):
        from ico import ICO96_DEFAULT
        return self._ico96 or ICO96_DEFAULT

    @attrcache
    def career(self):
        from career import career_current
        if self.cid == CID_USER:
            return career_current(self.id)

    @attrcache
    def info(self):
        from user_info import UserInfo
        id = self.id
        return UserInfo.mc_get(id)

    def pronoun(self, user_id):
        zsite_id = self.id
        if zsite_id == user_id:
            return '我'
        info = self.info
        if info and info.sex == 2:
            return '她'
        return '他'


def user_can_reply(user):
    return user.state >= ZSITE_STATE_CAN_REPLY
#
#class Zpage(McModel):
#    pass
#

def zsite_is_verify(id):
    zsite = Zsite.mc_get(id)
    return zsite.state >= ZSITE_STATE_VERIFY

def zsite_new(name, cid, state):
    zsite = Zsite(id=gid(), cid=cid, name=name, state=state)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_name_edit(id, name):
    from feed_po import mc_feed_user_dict
    if id:
        zsite = Zsite.mc_get(id)
        if zsite:
            zsite.name = name
            zsite.save()
            mc_feed_user_dict.delete(id)

def zsite_name_rm(id):
    from mail import rendermail
    from user_mail import mail_by_user_id
    zsite_name_edit(id, '无名')
    zsite = Zsite.mc_get(id)
    rendermail('/mail/notice/name_rm.txt', mail_by_user_id(id), zsite.name,
                   link=zsite.link,
                  )

def zsite_new_site(name, admin_id, state=ZSITE_STATE_APPLY):
    from zsite_admin import zsite_admin_new
    site = zsite_new(name, CID_SITE, state)
    zsite_admin_new(site.id, admin_id)
    return site

def zsite_rm_site(zsite_id):
    from zsite_admin import zsite_rm_site_extra
    o = Zsite.mc_get(zsite_id)
    if o and o.cid == CID_SITE and o.state >= ZSITE_STATE_APPLY:
        o.state = ZSITE_STATE_BAN
        o.save()
        zsite_rm_site_extra(zsite_id)


def zsite_new_user(name, state=ZSITE_STATE_APPLY):
    return zsite_new(name, CID_USER, state)

#def zsite_to_verify_by_cid(cid, limit, offset):
#    return Zsite.where(cid=cid, state=ZSITE_STATE_WAIT_VERIFY).order_by('id')[offset: limit+offset]
#
#def zsite_to_verify_count_by_cid(cid):
#    return Zsite.where(cid=cid, state=ZSITE_STATE_WAIT_VERIFY).count()


ZSITE_VERIFY_TEMPLATE = {
    CID_USER: {
        ZSITE_STATE_VERIFY: '/mail/verify/user_yes.txt',
        ZSITE_STATE_FAILED_VERIFY: '/mail/verify/user_no.txt',
    }
}

def zsite_verify_yes(zsite):
    zsite.state = ZSITE_STATE_VERIFY
    zsite.save()
    zsite_verify_mail(zsite.id, zsite.cid, zsite.state)

def zsite_verify_no(zsite, txt):
    zsite.state = ZSITE_STATE_FAILED_VERIFY
    zsite.save()
    zsite_verify_mail(zsite.id, zsite.cid, zsite.state, txt)

def zsite_verify_no_without_notify(zsite):
    zsite.state = ZSITE_STATE_FAILED_VERIFY
    zsite.save()


def zsite_verify_mail(zsite_id, cid, state, txt=''):
    from mail import rendermail
    from user_mail import mail_by_user_id
    template = ZSITE_VERIFY_TEMPLATE.get(cid, {}).get(state)
    if template:
        name = Zsite.mc_get(zsite_id).name
        mail = mail_by_user_id(zsite_id)
        rendermail(template, mail, name,
                   txt=txt,
                  )

from mq import mq_client
mq_zsite_verify_mail = mq_client(zsite_verify_mail)

if __name__ == '__main__':
    #zsite_name_rm(10017321)
    pass
