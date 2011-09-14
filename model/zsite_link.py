#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX
from oauth import OAUTH2NAME_DICT, OAUTH_DOUBAN, OAUTH_SINA,\
OAUTH_QQ, OAUTH_TWITTER
from model.zsite_url import link

OAUTH_LINK_DEFAULT = (
    OAUTH_DOUBAN    ,
    OAUTH_SINA      ,
    OAUTH_QQ        ,
    OAUTH_TWITTER   ,
)

OAUTH2NAME = tuple(
    (k, OAUTH2NAME_DICT[k]) for k in OAUTH_LINK_DEFAULT
)


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


def name_link_by_zsite_id(zsite_id, prefix=''):
    r = []
    _link = link(zsite_id)
    for id, name in link_id_name_by_zsite_id(zsite_id):
        r.append((
            name,
            '%s%s/link/%s'%(prefix, _link, id),
        ))
    return r

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

#def link_cid_new(zsite_id, name, link):
#    z = ZsiteLink.get_or_create(ziste_id=zsite_id, name=name)
#    z.link = link
#    z.save()
#    mc_flush(zsite_id)
#    return z
#
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

def link_cid_new(zsite_id, cid, link):
    link = link.strip()
    if link:
        zsite_link = ZsiteLink.get_or_create(zsite_id=zsite_id, cid=cid)
        zsite_link.link = link
        zsite_link.name = OAUTH2NAME_DICT[cid]
        zsite_link.save()
        mc_link_by_id.delete(zsite_link.id)
    mc_flush(zsite_id)


if __name__ == '__main__':
    #print link_id_cid(1)
    #print link_id_name_by_zsite_id(1)

    pass
    #link_cid_new(1, OAUTH_RENREN, "http://1.zuroc.xxx/i/link")
    #print link_id_name_by_zsite_id(1)
    #print link_id_cid(1)
    #print link_id_name_by_zsite_id(10000000)
    #print link_name_by_zsite_id(10000000)
    #http://zuroc.zuroc.xxx/link/8

    #print zhendi
    #print link_id_name_by_zsite_id(10000000)
