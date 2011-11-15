#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from po import Po
from cid import CID_PRODUCT,CID_COM
import json
from zsite_show import zsite_show_get,zsite_show_list
from itertools import  chain


class Product(McModel):
    pass

def product_new(product_id,_info_json):
    p = Product(id=product_id)
    p.info_json = json.dumps(dict(iter(_info_json)))
    p.save()
    return p


def product_by_com_id(com_id):
    po_product = Po.where(cid=CID_PRODUCT,zsite_id=com_id)
    if po_product:
        return Product.mc_get_list([i.id for i in po_product])

def product_all(limit=None,offset=None):
    com_list = zsite_show_list(CID_COM)
    if com_list:
        com_id_list = [c.id for c in com_list]
        if com_id_list:
            return chain.from_iterable([product_by_com_id(c) for c in com_id_list])

