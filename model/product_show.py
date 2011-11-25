#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, cursor_by_table, McCacheA, McLimitA, McNum, McCacheM

PRODUCT_SHOW_RM_STATE = 3
PRODUCT_SHOW_STATE = 4

class ProductShow(McModel):
    pass


def product_show_new(product_id,com_id,state=PRODUCT_SHOW_STATE,admin_id=0,rank=1):
    ps = ProductShow.get_or_create(id = product_id)
    ps.state = state
    ps.admin_id = admin_id
    ps.rank = rank
    ps.com_id = com_id
    ps.save()
    return ps

def product_show_id_list(limit=None,offset=None):
    return ProductShow.where(state>=PRODUCT_SHOW_STATE).order_by(rank desc).col_list(limit,offset,'id')

def product_show_list(limit=None,offset=None):
    return ProductShow.mc_get_list(product_show_id_list(limit,offset))

def product_show_rm(id,admin_id):
    ps = ProductShow.mc_get(id)
    if ps:
        ps.state = PRODUCT_SHOW_RM_STATE
        ps.admin_id = admin_id
        ps.save()
        return True

def product_show_id_by_com_id(com_id):
    return ProductShow.where(state>=PRODUCT_SHOW_STATE,com_id=com_id).order_by(rank,desc).col_list(col='id')
