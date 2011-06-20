#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zsite_list import ZsiteList, zsite_list, zsite_list_new, zsite_list_rm, zsite_list_get, zsite_list_rank

OWNER_ID = 0

def zsite_show(cid, limit=None, offset=None):
    return zsite_list(0, cid, limit, offset)

def zsite_show_new(zsite_id, rank=1000):
    cid_list = [] # TODO
    zsite_list_new(zsite_id, 0, cid_list, rank)

def zsite_show_rm(zsite_id):
    zsite_list_rm(zsite_id, 0)

def zsite_show_get(zsite_id):
    return zsite_list_get(zsite_id, 0, 0)

def zsite_show_rank(zsite_id, rank):
    zsite_list_rank(zsite_id, 0, rank)
