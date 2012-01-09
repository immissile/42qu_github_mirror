#coding:utf-8
import _env
from zkit.single_process import single_process
from model.po import Po
from model.site_sync import SiteSync
from model.sync import sync_site_po
from zkit.single_process import single_process
from model.zsite import Zsite
from model.kv_misc import KV_SYNC_SITE_PO_BY_ZSITE_ID, kv_int_call
from zweb.orm import ormiter
from config import ZSITE_BIND_FOR_SYNC

def _sync_site_po(begin_id):
    ss = SiteSync.where('id>%s', begin_id).order_by('id')[0]
    if ss:
        begin_id = ss.id
        zsite = Zsite.mc_get(ZSITE_BIND_FOR_SYNC)
        if zsite:
            po = Po.mc_get(ss.po_id)
            if po:
                sync_site_po(po, zsite)
        return begin_id


@single_process
def main():
    kv_int_call(KV_SYNC_SITE_PO_BY_ZSITE_ID, _sync_site_po)

if __name__ == '__main__':
    main()
