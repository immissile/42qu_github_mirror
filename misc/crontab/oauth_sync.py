#coding:utf-8
import _env
from zkit.single_process import single_process
from model.kv_misc import KV_SYNC_PO_BY_ZSITE_ID ,\
KV_SYNC_JOIN_EVENT_BY_ZSITE_ID ,\
KV_SYNC_RECOMMEND_BY_ZSITE_ID ,\
kv_int_call
from zweb.orm import ormiter
from model.po import Po
from model.state import STATE_ACTIVE
from model.sync import sync_po, sync_join_event,\
sync_recommend, sync_follow, SyncFollow
from model.cid import CID_WORD, CID_NOTE, CID_EVENT
from model.event import EventJoiner, EVENT_JOIN_STATE_NO
from model.feed import Feed

def _sync_po(begin_id):
    for po in ormiter(
        Po, 'id>%s and state=%s and cid in (%s,%s,%s)' % (
            begin_id, STATE_ACTIVE, CID_WORD, CID_NOTE, CID_EVENT
        )
    ):
        begin_id = po.id
        sync_po(po)

    return begin_id


def _sync_join_event(begin_id):
    for i in ormiter(
        EventJoiner,
        'id>%s and state>%s'%(
            begin_id, EVENT_JOIN_STATE_NO
        )
    ):
        begin_id = i.id
        sync_join_event(i.user_id, i.event_id)
    return begin_id

def _sync_recommend(begin_id):
    for i in ormiter(Feed,
        'id>%s and rid!=0'%(
            begin_id,
        )
    ):
        begin_id = i.id
        sync_recommend(i.zsite_id, i.rid)
    return begin_id



@single_process
def main():
    kv_int_call(KV_SYNC_PO_BY_ZSITE_ID, _sync_po)
    kv_int_call(KV_SYNC_JOIN_EVENT_BY_ZSITE_ID, _sync_join_event)
    kv_int_call(KV_SYNC_RECOMMEND_BY_ZSITE_ID, _sync_recommend)

    for i in SyncFollow.where('oauth_id!=0'):
        sync_follow(i)

if __name__ == '__main__':
    main()


