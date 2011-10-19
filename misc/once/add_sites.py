#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.zsite_site import site_new
from model.oauth import linkify
from model.motto import motto_set
from model.ico import site_ico_new, site_ico_bind
from model.zsite_link import link_list_save
from zkit.pic import picopen
import urllib

def make_site(name,link,motto,img_src,current_user_id=10017321):
    f = urllib.urlopen(img_src).read()
    if  f:
        pic = picopen(f)
        if pic:
            pic_id = site_ico_new(10017321,pic)
    site = site_new(name,current_user_id,sitetype=40)
    site_id = site.id
    link_cid = (2,'豆瓣小站',linkify(link,2))
    site_ico_bind(current_user_id, pic_id, site_id)
    link_list_save(site_id,link_cid,[])
    motto_set(site_id, motto)
    print site_id



if __name__ == "__main__":
    make_site()

