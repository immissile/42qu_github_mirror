#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, cursor_by_table, McCacheA, McLimitA, McNum, McCacheM
from po import Po


class ProductShow(Model):
    pass


def product_show_new(product_id,rank=1):
    ps = ProductShow.get_or_create(id = product_id)
    ps.rank = rank
    ps.save()
    return ps

def product_show_id_list(limit=None,offset=None):
    return ProductShow.where().order_by('rank desc').col_list(limit,offset,'id')

def product_show_list(limit=None,offset=None):
    return Po.mc_get_list(product_show_id_list(limit,offset))

def product_show_rm(product_id):
    ps = ProductShow.get(id=product_id)
    if ps:
        ps.delete()
        ps.save()
        return True


if __name__ == "__main__":
    #print product_show_rm(12)
    print product_show_list()
    #print product_show_id_list()
    #product_show_new(13)
