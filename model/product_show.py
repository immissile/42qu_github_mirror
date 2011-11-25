#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, cursor_by_table, McCacheA, McLimitA, McNum, McCacheM
from po import Po
from cid import CID_PRODUCT

class ProductShow(McModel):
    pass

mc_product_show_get = McCache('ProductNewGet:%s')
mc_product_show_id_list = McLimitA('ProductShowIdList:%s',512)
product_show_count = McNum(lambda x: ProductShow.where("rank>0").count(), 'ProductShowCount:%s')


def product_show_new(product, rank=None):
    id = product.id

    if product.cid != CID_PRODUCT:
        return

    ps = ProductShow.get_or_create(id=id)

    if rank is None:
        c = ProductShow.raw_sql('select max(rank) from product_show')
        r = c.fetchone()
        if r:
            rank = r[0]+1
        else:
            rank = 1

    ps.rank = rank

    ps.save()
    mc_flush(id)
    return ps

@mc_product_show_id_list('')
def product_show_id_list(com_id=0, limit=None, offset=None):
    q = ProductShow.where('rank>0')
    return q.order_by('rank desc').col_list(limit, offset, 'id')

def product_show_list(limit=None, offset=None):
    return Po.mc_get_list(product_show_id_list(com_id, limit, offset))

def product_show_rm(product):
    id = product.id

    if product.cid != CID_PRODUCT:
        return

    ProductShow.where(id=id).delete()
    mc_flush(id)

def mc_flush(id):
    mc_product_show_get.delete(id)
    mc_product_show_id_list.delete('')

@mc_product_show_get('{id}')
def product_show_get(id):
    i = ProductShow.mc_get(id)
    if i:
        return i.rank
    return 0


if __name__ == '__main__':
    #print product_show_rm(12)
    #print product_show_list()
    #print product_show_id_list()
    #product_show_new(13)

    print product_show_count()
