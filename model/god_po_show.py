#coding:utf-8
import _db
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

def po_show_zsite_channel():
    return Zsite.mc_get_list(PO_SHOW_ZSITE_CHANNEL)
