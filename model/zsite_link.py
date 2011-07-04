#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache
from hashlib import sha256
from zsite import zsite_new_user, Zsite
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX


mc_link_id_name = McCache("LinkIdName:%s")
mc_link_id_cid = McCache("LinkIdCid:%s")
mc_link_by_id = McCache("LinkById:%s")

def mc_flush(zsite_id):
    mc_link_id_name.delete(zsite_id)

class ZsiteLink(Model):
    pass

@mc_link_id_name("{zsite_id}")
def link_id_name_by_zsite_id(zsite_id):
    c = ZsiteLink.raw_sql('select id, name from zsite_link where zsite_id=%s', zsite_id)
    return c.fetchall()

@mc_link_by_id("{id}")
def link_by_id(id):
    return  

def link_by_cid_id(id):
    return

if __name__ == "__main__":
    print link_id_name_by_zsite_id(1)


