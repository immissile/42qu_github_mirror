#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config.zpage_host import SITE_DOMAIN, SITE_DOMAIN_SUFFIX

def zsite_by_domain(domain):
    zsite = None
    if domain.endswith(SITE_DOMAIN_SUFFIX):
        domain = domain[:-len(SITE_DOMAIN_SUFFIX)]
        if domain.isdigit():
            zsite = Zsite.mc_get(domain)
    return zsite

@property
def _link(self):
    if not hasattr(self, "_link"):
        self._link = "http://%s.%s"%(self.id, SITE_DOMAIN)
    return self._link

Zsite.link = _link

if __name__ == "__main__":
    pass





