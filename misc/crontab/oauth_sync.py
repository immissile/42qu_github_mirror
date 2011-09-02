#coding:utf-8
from zkit.single_process import single_process
from model.kv_misc import KV_SYNC_PO_BY_ZSITE_ID ,\
KV_SYNC_JOIN_EVENT_BY_ZSITE_ID ,\
KV_SYNC_RECOMMEND_BY_ZSITE_ID ,\
KV_SYNC_FOLLOW_BY_SYNC_ID ,\
kv_int_call

#mq_sync_po_by_zsite_id = mq_client(sync_po_by_zsite_id)
#mq_sync_join_event_by_zsite_id = mq_client(sync_join_event_by_zsite_id)
#mq_sync_recommend_by_zsite_id = mq_client(sync_recommend_by_zsite_id)
#mq_sync_follow_by_sync_id = mq_client(sync_follow_by_sync_id)

def sync_po_by_zsite_id(begin_id):
    pass


def sync_join_event_by_zsite_id(begin_id):
    pass


def sync_recommend_by_zsite_id(begin_id):
    pass


def sync_follow_by_sync_id(begin_id):
    pass



@single_process
def main():
    kv_int_call(KV_SEO_PING, ping_po)


if __name__ == "__main__":
    pass



