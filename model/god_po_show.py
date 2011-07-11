#coding:utf-8
from _db import McCache
from zsite import Zsite

PO_SHOW_ZSITE_CHANNEL = (
10045702 ,
10045703 ,
10045704 ,
10045705 ,
10045706 ,
10045707 ,
10045708 ,
10045709 ,
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
