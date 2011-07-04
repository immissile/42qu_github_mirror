#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX

OAUTH_GOOGLE = 1
OAUTH_DOUBAN = 2
OAUTH_SINA = 3
OAUTH_TWITTER = 4
OAUTH_WWW163 = 5
OAUTH_BUZZ = 6
OAUTH_SOHU = 7
OAUTH_QQ = 8
OAUTH_RENREN = 9
OAUTH_LINKEDIN = 10

OAUTH2NAME = (
    (OAUTH_DOUBAN, '豆瓣'),
    (OAUTH_SINA, '新浪微博'),
    (OAUTH_QQ, '腾讯微博'),
    (OAUTH_BUZZ, 'Google+'),
    (OAUTH_TWITTER, 'Twitter'),
    (OAUTH_LINKEDIN, 'LinkedIn'),

)
OAUTH2NAME_DICT = dict(OAUTH2NAME)


mc_link_id_name = McCache('LinkIdName:%s')
mc_link_id_cid = McCache('LinkIdCid:%s')
mc_link_by_id = McCache('LinkById:%s')


def mc_flush(zsite_id):
    mc_link_id_name.delete(zsite_id)
    mc_link_id_cid.delete(zsite_id)

class ZsiteLink(Model):
    pass


@mc_link_id_name('{zsite_id}')
def link_id_name_by_zsite_id(zsite_id):
    c = ZsiteLink.raw_sql('select id, name from zsite_link where zsite_id=%s', zsite_id)
    return c.fetchall()


@mc_link_by_id('{id}')
def link_by_id(id):
    link = ZsiteLink.get(id)
    return link.link


@mc_link_id_cid('{id}')
def link_id_cid(id):
    c = ZsiteLink.raw_sql(
        'select id, cid from zsite_link where zsite_id=%s and cid>0', id
    )
    return c.fetchall()


def link_list_save(zsite_id, link_cid, link_kv):
    for cid, name, link in link_cid:
        zsite_link = ZsiteLink.get_or_create(zsite_id=zsite_id, cid=cid)
        if not link:
            if zsite_link.id:
                zsite_link.delete()
            continue
        zsite_link.link = link
        zsite_link.name = name
        link_id = zsite_link.id
        zsite_link.save()
        if link_id:
            mc_link_by_id.delete(link_id)

    for id, name, link in link_kv:
        if id:
            if not name or not link:
                ZsiteLink.where(id=id, zsite_id=zsite_id).delete()
            else:
                ZsiteLink.where(id=id, zsite_id=zsite_id).update(name=name, link=link)
            mc_link_by_id.delete(id)
        elif name and link:
            zsite_link = ZsiteLink(zsite_id=zsite_id, name=name, link=link).save()
            zsite_link.save()

    mc_flush(zsite_id)



if __name__ == '__main__':
    print link_id_cid(1)
    print link_id_name_by_zsite_id(1)
