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
    #zsite_name_rm(10017321)
    #print zsite_user_verify_count()
    from zweb.orm import ormiter
    from model.ico import  pic_url, ico_save, picopen
    from os.path import exists
    from model.cid import CID_TAG
    from collections import defaultdict

    o = Zsite.get(cid=CID_TAG)
    print o.link
#    o = Zsite.mc_get(10224276)

#    s = """10228391 Django / 框架 -->> Django
#10229276 Express / 框架 -->> Express
#
#10221720 索尼爱立信 / Sony Ericsson -->> x
#10229578 索爱 / Sony Ericsson -->> 索尼爱立信 / Sony Ericsson / 索爱
#
#10226590 拉拉 / lesbian -->> 拉拉 / 蕾丝边 / lesbian 
#10233537 Lesbian -->> x
#
#10232779 LEGO -->> x
#10233139 乐高 / LEGO -->> 
#
#10223165 新蛋网 / Newegg -->> 新蛋 / Newegg 
#10232928 Newegg -->> x
#
#10231103 Android / 操作系统 -->> Android / 安卓
#10234061 iQQ / 操作系统 -->> iQQ
#
#10221959 康泰纳仕 / Conde Nast -->> 
#10228320 Conde Nast -->> x
#
#10222435 Eric Schmidt -->> x
#10231156 埃里克·施密特 / Eric Schmidt -->> 
#
#10221528 工商管理硕士 / MBA -->> 
#10230864 MBA -->> x
#
#10222458 GIS / 地理信息系统 -->> 
#10232868 GIS -->> x
#
#10221952 愤怒的小鸟 / Angry Birds -->> 
#10231718 Angry Birds -->> x
#
#10222432 中国国际数码互动娱乐产品及技术应用展览会 / ChinaJoy -->> 
#10226839 Chinajoy -->> x
#
#10222562 音乐播放器 / 硬件 -->> 音乐播放器
#10224057 产品设计 / 硬件 -->> 产品设计 / Product Design
#
#10222186 mfc sdk  c/c++ -->> mfc / sdk
#10227358 C / C++ -->> C & C++
#10230686 C++ -->> x
#
#10221390 三国志  -->> 
#10223964 三国志 / 史书 -->> x
#
#10224219 Color  -->> Color / 颜色
#10228494 Color -->> x
#
#10232103 Nikon -->> x
#10233608 尼康 / Nikon -->> 
#
#10223150 MOTO Defy  / ME525/MB525 -->> MOTO Defy / 摩托罗拉 Defy
#10223288 ME525 -->> x
#
#10220771 Java 虚拟机 / JVM -->> 
#10224387 Java 虚拟机 -->> x
#
#10228073 本格 / 推理小说流派 -->> 本格 / 新本格 / 推理小说 / 侦探小说
#10231417 新本格 / 推理小说流派 -->> x
#
#10224601 App Store -->> x
#10232016 软件商店 / App Store -->> 
#
#10221852 键盘 / 计算机 -->> 键盘
#10227476 键盘 / 乐器 -->> x
#
#10220920 亚马逊软件商店 / Android -->> 亚马逊软件商店 / Android软件商店 / Android App Store
#10231103 Android / 操作系统 -->> Android / 安卓
#
#10222979 How To -->> x
#10224695 如何 / How To -->> 
#
#10224063 Fancy -->> Fancy
#10228451 Fancy / 网站 -->> x
#
#10227757 苹果 / 水果 -->> x
#
#10223867 Jonathan Ive -->> x
#10232890 乔纳森·艾弗 / Jonathan Ive -->> 
#
#10227476 键盘 / 乐器 -->> 键盘 / keyboard
#10231052 笛 / 乐器 -->> 笛 / 笛子
#
#10225548 魔兽世界 / World of Warcraft / WOW -->> 
#10233973 WOW -->> x
#
#10227124 谷歌公司 / Google -->> 谷歌 / Google
#10233600 Google -->> x
#
#10223039 Readability -->> x
#10231499 可读性 / Readability -->> 
#
#10225244 互联网数据中心 / IDC -->> 
#10231479 IDC -->> x
#
#10220913 CFD -->> x
#10233487 计算流体力学 / CFD -->> 
#
#10228703 扎客 / Zaker -->> 
#10233753 Zaker -->> x
#
#10228451 Fancy / 网站 -->> Fancy
#10231910 下厨房 / 网站 -->> 下厨房
#
#10221035 优衣库 / UNIQLO -->> 
#10229280 Uniqlo -->> x
#
#10227358 C / C++ -->> C & C++
#10234409 C  -->> x
#
#10225242 VJIA / V+ -->> x
#10232002 V+ / 凡客诚品旗下 -->> 凡客诚品 &VJIA
#
#10225384 宜家家居 / IKEA -->> x
#10228882 宜家 / IKEA -->> 宜家 / IKEA
#
#10222562 音乐播放器 / 硬件 -->> x
#10226329 音乐播放器  -->> 
#
#10221168 联邦快递 / FedEx -->> 
#10222735 FedEx -->> x
#
#10230261 Java  -->> 
#10231395 Swing / Java -->> Swing
#
#10229286 高清 / HD -->> 
#10231825 HD -->> x"""
#
#    s = s.split('\n')
#    for i in s:
#        if not i.strip():
#            continue
#        i, x = i.split('-->>')
#        id = i.split(' ')[0]
#        if x.endswith(' x'):
#            Zsite.where(id=id).delete()
#        elif not x.strip():
#            continue
#        else:
#            x = x.strip()
#            z = Zsite.mc_get(id)
#            z.name = x
#            z.save()
#    raise

    #小写
    #别名
    #/
#    name_map = defaultdict(list)
#    count = 0
#    for zsite in ormiter(Zsite, 'cid=%s'%CID_TAG):
#        name = zsite.name.replace(' I/O', 'IO').replace('TCP/IP', 'TCP-IP')
#        zsite.save()
#        name_s = map(str.lower, map(str.strip, name.split('/')))
#
#        for i in name_s:
#            if i != name:
#                name_map[i].append(zsite.id)
#
#    for k, v in name_map.iteritems():
#        if len(v) > 1:
#            for i in Zsite.mc_get_list(v):
#                print i.id , i.name , '-->> '
#            print ''


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




