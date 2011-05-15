#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from hashlib import sha256
from zsite import zsite_new_user, Zsite

def zsite_id_by_domain():
    pass

@property
def _link(self):
    if not hasattr(self, "_link"):
        self._link = "http://%s.%s"%(self.id, SITE_DOMAIN)
    return self._link

Zsite.link = _link

if __name__ == "__main__":
    pass





