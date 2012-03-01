#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import escape
from cid import CID_USER
from _db import Model, McModel
from gid import gid
from txt import txt_property
from zkit.attrcache import attrcache

ZSITE_STATE_BAN = 1
ZSITE_STATE_NO_PASSWORD = 6
ZSITE_STATE_APPLY = 10
ZSITE_STATE_ACTIVE = 15
ZSITE_STATE_FAILED_VERIFY = 20
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


def zsite_name_edit(id, name):
    from feed_po import mc_feed_user_dict
    if id:
        zsite = Zsite.mc_get(id)
        if zsite:
            cid = zsite.cid
            if cid == CID_USER:
                name = name.decode('utf-8', 'ignore')[:24]
            zsite.name = name
            zsite.save()
            mc_feed_user_dict.delete(id)
            from zsite_verify import zsite_verify_ajust
            zsite_verify_ajust(zsite)


def zsite_name_rm(id):
    from mail import rendermail
    from user_mail import mail_by_user_id
    from zsite_url import url_by_id
    url = url_by_id(id)
    if url:
        zsite_name_edit(id, url)
    else:
        zsite_name_edit(id, '')
    zsite = Zsite.mc_get(id)
    rendermail(
        '/mail/notice/name_rm.txt',
        mail_by_user_id(id),
        zsite.name,
        link=zsite.link,
    )

def zsite_by_query(query):
    from config import SITE_DOMAIN
    from urlparse import urlparse
    from model.zsite_url import id_by_url
    from model.user_mail import user_id_by_mail
    user_id = None

    if '@' in query:
        user_id = user_id_by_mail(query)
    elif SITE_DOMAIN in query:
        key = urlparse(query).netloc.split('.', 1)[0]
        user_id = id_by_url(key)
    elif query.isdigit():
        if Zsite.mc_get(query):
            user_id = query
    else:
        query = query.replace('http://', '')
        user_id = id_by_url(query)

    return user_id


def zsite_new(name, cid, state=ZSITE_STATE_APPLY, id=None):
    if id is None:
        id = gid()
    zsite = Zsite(id=id, cid=cid, name=name, state=state)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_new_user(name, state=ZSITE_STATE_APPLY):
    from model.autocomplete_user import autocomplete_user_name_new
    user = zsite_new(name, CID_USER, state)
    autocomplete_user_name_new(user, 0) 
    return user

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
#
#def zsite_verify_yes(zsite):
#    zsite.state = ZSITE_STATE_VERIFY
#    zsite.save()
#    zsite_verify_mail(zsite.id, zsite.cid, zsite.state)
#
#def zsite_verify_no(zsite, txt):
#    zsite.state = ZSITE_STATE_FAILED_VERIFY
#    zsite.save()
#    zsite_verify_mail(zsite.id, zsite.cid, zsite.state, txt)
#
#def zsite_verify_no_without_notify(zsite):
#    zsite.state = ZSITE_STATE_FAILED_VERIFY
#    zsite.save()
#
def zsite_user_verify_count():
    count = Zsite.raw_sql( 'select count(1) from zsite where cid=%s and state=%s'%( CID_USER, ZSITE_STATE_VERIFY ) ).fetchone()[0]
    return count

def zsite_name_id_dict(id_set):
    d = Zsite.mc_get_dict(id_set)
    r = {}
    for i in id_set:
        t = d[i]
        if t is not None:
            r[i] = t.name
    return r

#from mq import mq_client
#mq_zsite_verify_mail = mq_client(zsite_verify_mail)
#
#def zsite_verify_mail(zsite_id, cid, state, txt=''):
#    from mail import rendermail
#    from user_mail import mail_by_user_id
#    template = ZSITE_VERIFY_TEMPLATE.get(cid, {}).get(state)
#    if template:
#        name = Zsite.mc_get(zsite_id).name
#        mail = mail_by_user_id(zsite_id)
#        rendermail(template, mail, name,
#                   txt=txt,
#                  )

if __name__ == '__main__':
    pass
    
    #zsite_name_rm(10017321)
    #print zsite_user_verify_count()
#    from zweb.orm import ormiter
#    from model.ico import  pic_url, ico_save, picopen
#    from os.path import exists
#    from model.cid import CID_TAG
#    from collections import defaultdict
    from zweb.orm import ormiter
    from model.ico import  pic_url, ico_save, picopen
    from os.path import exists
    from model.cid import CID_TAG
    from collections import defaultdict

    zsite_new_user("test", state=ZSITE_STATE_APPLY)

    #id = 10224057
  #  id = 10232186 
  #  o = Zsite.mc_get(id)

  #  print o.name


#    s = """10228391 Django / 框架 -->> Django
#10229276 Express / 框架 -->> Express
#
#
#    s = map(int,s.split("\n"))
#
#    print s
#    for i in s:
#        Zsite.where(id=i).delete()
#
#    #id = 10224057
#  #  id = 10232186 
#  #  o = Zsite.mc_get(id)
#
#  #  print o.name
#
#    raise
#
#    #小写
#    #别名
#    #/
#    name_map = defaultdict(list)
#    count = 0
#    for zsite in ormiter(Zsite, 'cid=%s'%CID_TAG):
#        name = zsite.name.replace(' I/O', 'IO').replace('TCP/IP', 'TCP-IP')
#        zsite.save()
#        name_s = map(str.lower, map(str.strip, name.split('/')))
#
#        id = zsite.id
#        for i in name_s:
#            name_map[i].append(id)
#
#    for k, v in name_map.iteritems():
#        if len(v) > 1:
#            for i in Zsite.mc_get_list(v):
#                print i.id , i.name , '-->> '
#            print ''

  #  print name_map["产品设计"]
  #  print name_map["产品设计"]

#    for line in """
#/mnt/zpage/721/557/186925.jpg
#/mnt/zpage/721/142/185486.jpg
#/mnt/zpage/721/159/186527.jpg
#/mnt/zpage/721/813/187181.jpg
#""".strip().split():
#        path = line.replace('/721/', '/0/')
#        if exists(path):
#            id = path.rsplit('/', 1)[-1][:-4]
#            img = picopen(open(path).read())
#            print id
#            ico_save(id, img)

#for i in ormiter(Zsite):
#    s = pic_url(i.id, 721)
#    if s is not None:
#        path = '/mnt/zpage/%s'%s[18:]
#        if not  exists(path):
#            print path


