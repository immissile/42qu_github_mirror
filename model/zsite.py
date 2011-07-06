#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cgi import escape
from cid import CID_USER
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
    def ico96(self):
        from ico import ico_url_with_default
        return ico_url_with_default(self.id)

    @attrcache
    def career(self):
        from career import career_current
        if self.cid == CID_USER:
            return career_current(self.id)


def user_can_reply(user):
    return user.state >= ZSITE_STATE_CAN_REPLY
#
#class Zpage(McModel):
#    pass
#

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

def zsite_new_user(name):
    return zsite_new(name, CID_USER, ZSITE_STATE_APPLY)

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
    if zsite.state == ZSITE_STATE_WAIT_VERIFY:
        zsite.state = ZSITE_STATE_VERIFY
        zsite.save()
        mq_zsite_verify_mail(zsite.id, zsite.cid, zsite.state)

def zsite_verify_no(zsite, txt):
    if zsite.state == ZSITE_STATE_WAIT_VERIFY:
        zsite.state = ZSITE_STATE_FAILED_VERIFY
        zsite.save()
        mq_zsite_verify_mail(zsite.id, zsite.cid, zsite.state, txt)

def zsite_verify_mail(zsite_id, cid, state, txt=''):
    from mail import rendermail
    from user_mail import mail_by_user_id
    template = ZSITE_VERIFY_TEMPLATE.get(cid, {}).get(state)
    if template:
        name = Zsite.mc_get(user_id).name
        mail = mail_by_user_id(user_id)
        rendermail(template, mail, name,
                   txt=txt,
                  )

from mq import mq_client
mq_zsite_verify_mail = mq_client(zsite_verify_mail)

if __name__ == "__main__":
    zsite = Zsite.mc_get(1)
    zsite.state = ZSITE_STATE_WAIT_VERIFY
    zsite_verify_yes(zsite)

