#coding:utf-8
from zkit.single_process import single_process
from model.kv_misc import KV_SYNC_PO_BY_ZSITE_ID ,\
KV_SYNC_JOIN_EVENT_BY_ZSITE_ID ,\
KV_SYNC_RECOMMEND_BY_ZSITE_ID ,\
KV_SYNC_FOLLOW_BY_SYNC_ID ,\
kv_int_call
from zweb.orm import ormiter
from model.po import Po
from model.state import STATE_ACTIVE
from model.sync import sync_po, sync_join_event_by_zsite_id, \
sync_recommend_by_zsite_id, sync_follow_by_sync_id

def sync_po_by_zsite_id(begin_id):
    for po in ormiter(
        Po, 'id>%s and state=%s' % (begin_id, STATE_ACTIVE)
    ):
        begin_id = po.id
        #sync_po(po) 
    return begin_id


def sync_join_event_by_zsite_id(begin_id):
    return begin_id


def sync_recommend_by_zsite_id(begin_id):
    return begin_id


def sync_follow_by_sync_id(begin_id):
    return begin_id



@single_process
def main():
    kv_int_call(KV_SYNC_PO_BY_ZSITE_ID, sync_po_by_zsite_id)
    kv_int_call(KV_SYNC_JOIN_EVENT_BY_ZSITE_ID, sync_join_event_by_zsite_id)
    kv_int_call(KV_SYNC_RECOMMEND_BY_ZSITE_ID, sync_recommend_by_zsite_id)
    kv_int_call(KV_SYNC_FOLLOW_BY_SYNC_ID, sync_follow_by_sync_id)


if __name__ == "__main__":
    pass



