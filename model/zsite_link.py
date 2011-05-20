#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX

class ZsiteUrl(Model):
    pass

mc_zsite_url_by_id = McCache('ZsiteUrlById.%s')
mc_zsite_id_by_url = McCache('ZsiteIdByUrl.%s')

@mc_zsite_url_by_id('{id}')
def zsite_url_by_id(id):
    z = ZsiteUrl.get(id)
    return z.url if z else ''

@mc_zsite_id_by_url('{url}')
def _zsite_id_by_url(url):
    z = ZsiteUrl.get(url=url)
    if z is None:
        return 0
    return z.id

def zsite_id_by_url(url):
    url = url.lower()
    return _zsite_id_by_url(url)

def zsite_url_new(id, url):
    id = int(id)
    url = url.lower()
    if zsite_id_by_url(url):
        return
#    if zsite_url_by_id(id):
#        return
    z = ZsiteUrl.get_or_create(id=id)
    z.url = url
    z.save()
    mc_zsite_id_by_url.set(url, id)
    mc_zsite_url_by_id.set(id, url)

def zsite_by_domain(domain):
    if domain.endswith(SITE_DOMAIN_SUFFIX):
        domain = domain[:-len(SITE_DOMAIN_SUFFIX)]
        if domain.isdigit():
            id = domain
        else:
            zsite_id = zsite_id_by_url(domain)
        return Zsite.mc_get(zsite_id)

@property
def _link(self):
    if not hasattr(self, "_link"):
        self._link = "http://%s.%s"%(self.id, SITE_DOMAIN)
    return self._link

Zsite.link = _link

if __name__ == "__main__":
    pass





