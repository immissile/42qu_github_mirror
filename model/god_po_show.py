#coding:utf-8
from _db import McCache
from zsite import Zsite


PO_SHOW_ZSITE_CHANNEL = (
10036807 ,
10036808 ,
10036809 ,
10036810 ,
10036811 ,
10036812 ,
10036813 ,
10036814 ,
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
