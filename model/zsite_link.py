#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX

class Url(Model):
    pass

mc_url_by_id = McCache('UrlById.%s')
mc_id_by_url = McCache('IdByUrl.%s')

@mc_url_by_id('{id}')
def url_by_id(id):
    u = Url.get(id)
    if u is None:
        return ''
    return u.url

@mc_id_by_url('{url}')
def _id_by_url(url):
    u = Url.get(url=url)
    if u is None:
        return 0
    return u.id

def id_by_url(url):
    url = url.lower()
    return _id_by_url(url)

def url_new(id, url):
    id = int(id)
    url = url.lower()
    if id_by_url(url):
        return
#    if url_by_id(id):
#        return
    u = Url.get_or_create(id=id)
    u.url = url
    u.save()
    mc_id_by_url.set(url, id)
    mc_url_by_id.set(id, url)

def zsite_by_domain(domain):
    if domain.endswith(SITE_DOMAIN_SUFFIX):
        domain = domain[:-len(SITE_DOMAIN_SUFFIX)]
        if domain.isdigit():
            zsite_id = domain
        else:
            zsite_id = id_by_url(domain)
        return Zsite.mc_get(zsite_id)

@property
def _link(self):
    if not hasattr(self, "_link"):
        self._link = "http://%s.%s"%(url_by_id(self.id) or self.id, SITE_DOMAIN)
    return self._link

Zsite.link = _link

if __name__ == "__main__":
    pass





