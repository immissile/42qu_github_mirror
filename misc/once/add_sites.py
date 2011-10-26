#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_site import site_new
from model.oauth import linkify
from model.motto import motto_set
from model.ico import site_ico_new, site_ico_bind
from model.zsite_link import ZsiteLink, mc_flush
from model.rss import rss_new, Rss
from zkit.pic import picopen
import urllib
import json
import time


def make_site(name,link,motto,img_src,site_num,current_user_id=10017321):
    f = urllib.urlopen(img_src).read()
    if  f:
        pic = picopen(f)
        if pic:
            pic_id = site_ico_new(10017321,pic)
    site = site_new(name,current_user_id,40)
    site_id = site.id
    site_ico_bind(current_user_id, pic_id, site_id)
    zsite_link = ZsiteLink.get_or_create(zsite_id=site_id,cid=2)
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
        like,link,img,name = info.get(id)
        if meta.get(id):
            motto = meta.get(id)[0][0]
            motto = motto.split('<br />')[0]
            img_src = meta.get(id)[0][1]
            make_site(name,link,motto,img_src,id)
        else:
            print id,'no motto data'
    else:
        print id,'数据未录入'

def check():
    s = set()
    for r in Rss.where():
        s.add(r.url.split('/')[-1] or r.url.split('/')[-2])
    with open('makeexcel.txt') as me:
        for i in me:
            i = i.strip()
            if i not in s:
                get_in(i)
                time.sleep(1)
    

def get_douban_site():
    zs = ZsiteLink.where(link='http://site.douban.com/110633/（1号厅的光影传奇）')
    if zs:
        zs = zs[0]
        zs.link = 'http://site.douban.com/110633/'
        zs.save()
    for zl in ZsiteLink.where(name='豆瓣小站').clo_list('zsite_id'):
        print Rss.where(user_id=zl).link 

if __name__ == "__main__":
    get_douban_site()
    #check()
    #get_in('106782')
