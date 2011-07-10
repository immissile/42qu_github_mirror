#coding:utf-8
from _db import McCache
from zsite import Zsite

PO_SHOW_ZSITE_CHANNEL = (
10033946 ,
10033947 ,
10033948 ,
10033949 ,
10033950 ,
10033951 ,
10033952 ,
10033953 ,
)

mc_po_show_zsite_channel = McCache("PoShowZsiteChannel:%s")

@mc_po_show_zsite_channel("")
def po_show_zsite_channel():
    return tuple(zip(
        PO_SHOW_ZSITE_CHANNEL,
        [
            i.name for i in
            Zsite.mc_get_list(PO_SHOW_ZSITE_CHANNEL)
        ]
    ))
