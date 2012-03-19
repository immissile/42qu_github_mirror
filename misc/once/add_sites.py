#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_site import site_new
from model.motto import motto_set
from model.ico import site_ico_new, site_ico_bind
from model.zsite_link import ZsiteLink, mc_flush
from model.site_po import po_cid_count_by_zsite_id
from model.zsite_admin import admin_id_list_by_zsite_id, zsite_admin_empty, zsite_admin_new
from model.zsite import Zsite
from model.zsite_show import zsite_show_rm, zsite_show_new
from model.zsite_fav import zsite_fav_rm_all_by_zsite_id
from model.cid import CID_SITE, CID_NOTE, CID_USER
from model.rss import rss_new, Rss
from zkit.pic import picopen
from model.zsite_site import zsite_site_rm
import urllib
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def make_site(name, link, motto, img_src, site_num, current_user_id=10017321):
    f = urllib.urlopen(img_src).read()
    if  f:
        pic = picopen(f)
        if pic:
            pic_id = site_ico_new(10017321, pic)
    site = site_new(name, current_user_id, 40)
    site_id = site.id
    site_ico_bind(current_user_id, pic_id, site_id)
    zsite_link = ZsiteLink.get_or_create(zsite_id=site_id, cid=2)
    zsite_link.link = link
    zsite_link.name = '豆瓣小站'
    zsite_link.save()
    mc_flush(site_id)
    motto_set(site_id, motto)
    rss_new(site_id, 'http://rss-tidy.42qu.com/douban/site/%s'%site_num, name, link, auto=1)
    print site_id

def get_in(id):
    with open('data/intro') as i:
        intro = json.loads(i.read())
    with open('data/info') as i:
        info = json.loads(i.read())
    with open('data/meta') as i:
        meta = json.loads(i.read())
    idintro = intro.get(id)
    if info.get(id):
        like, link, img, name = info.get(id)
        if meta.get(id):
            motto = meta.get(id)[0][0]
            motto = motto.split('<br />')[0]
            motto = motto.split('<a')[0]
            motto = motto.replace('豆瓣', '')
            motto = motto.replace('豆子', '')
            img_src = meta.get(id)[0][1]
            make_site(name, link, motto, img_src, id)
        else:
            print id, 'no motto data'
    else:
        print id, '数据未录入'

def check():
    s = set()
    for r in Rss.where():
        s.add(r.url.split('/')[-1] or r.url.split('/')[-2])
    with open('makeexcel.txt') as me:
        for i in me:
            i = i.strip()
            if i not in s:
                print r.user_id
                get_in(i)
                time.sleep(1)
            else:
                count = po_cid_count_by_zsite_id(r.user_id, CID_NOTE)
                if count == 0:
                    zsite_show_rm(Zsite.mc_get(r.user_id))
                    #zsite_fav_rm_all_by_zsite_id(r.user_id)
                    zsite_admin_empty(r.user_id)

                    print r.user_id, '!!'
                print i


def rm_same():
    sites = []
    result = {}
    for site in Zsite.where(cid=3, state=40):
        if site.name in result:
            sites.append([site.id, site.name])
        else:
            result[site.name] = site.id
    print len(sites)

    for i, j in sites:
        zsite_site_rm(i)
#rss = Rss.mc_get_list(sites)


def recover():
    rec = []
    for z in Zsite.where(cid=3, state=0):
        if Rss.get(user_id=z.id):
            rec.append(z)

    #  print rec
    rec_name = [i.name for i in rec]
    # print rec_name

    rm = []
    for z in Zsite.where(cid=3, state=40):
        if z.name in rec_name:
            rm.append(z)

    for z in rec:
        z.state = 40
        zsite_admin_new(z.id, 10017321)
        z.save()
        zsite_show_new(z.id, 3)

    for z in rm:
        zsite_site_rm(z.id)


def add_rss_url():
    pass


def get_douban_site():
    with open('data/intro') as i:
        intro = json.loads(i.read())
    with open('data/info') as i:
        info = json.loads(i.read())
    with open('data/meta') as i:
        meta = json.loads(i.read())
    #zs = ZsiteLink.where(link='http://site.douban.com/110633/（1号厅的光影传奇）')
    #if zs:
    #    zs = zs[0]
    #    zs.link = 'http://site.douban.com/110633/'
    #    zs.save()
    for zl in ZsiteLink.where(name='豆瓣小站').order_by('id desc').col_list(col='zsite_id'):
        if not Rss.where(user_id=zl):
            zs = ZsiteLink.raw_sql('select link from zsite_link where link like %s and zsite_id=%s and cid=2', 'http://site.douban.com%', zl).fetchone()
            if zs:
                id = zs[0].split('/')[-1] or zs[0].split('/')[-2]
                if info.get(id):
                    like, link, img, name = info.get(id)
                    if meta.get(id):
                        motto = meta.get(id)[0][0]
                        motto = motto.split('<br />')[0]
                        motto = motto.split('<a')[0]
                        img_src = meta.get(id)[0][1]
                        rss_new(zl, 'http://rss-tidy.42qu.com/douban/site/%s'%id, name, link, auto=1)
                        print zl, 'http://site.douban.com/%s'%id
                    else:
                        print id, 'no motto data'
                else:
                    print id, '数据未录入', zl
if __name__ == '__main__':
    #zsite_show_rm(Zsite.mc_get(10133601))
    #zsite_fav_rm_all_by_zsite_id(10133601)
    #zsite_admin_empty(10133601)
    recover()
    #for zl in ZsiteLink.where(name='豆瓣小站').clo_list('zsite_id'):
    #    print zl.link 
    #get_douban_site()
    #check()
    #get_in('106782')
