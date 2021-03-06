#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, Model, McCacheM, McCacheA
from po import Po, PO_CID
from model.state import STATE_PO_ZSITE_REVIEW_THEN_SHOW , STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.feed_render import render_zsite_feed_list
PAGE_LIMIT = 25
#mc_pos_id_list_by_cid = McCacheM("PosIdListByCid:%s")

mc_po_count_by_zsite_id = McCacheA('PoCountByZsiteId:%s')
mc_po_id_list_by_zsite_id = McLimitA('PoIdListByZsiteId.%s', 512)

def _po_cid_count_by_zsite_id(zsite_id, cid):
    qs = Po.where(
        zsite_id=zsite_id
    ).where('state>=%s'%STATE_PO_ZSITE_SHOW_THEN_REVIEW)
    if cid:
        qs = qs.where(cid=cid)
    return qs.count()

po_cid_count_by_zsite_id = McNum(_po_cid_count_by_zsite_id, 'PoIdCount:%s')

@mc_po_count_by_zsite_id('{zsite_id}')
def _po_count_by_zsite_id(zsite_id):
    return tuple(
        po_cid_count_by_zsite_id(zsite_id, i) for i in PO_CID
    )

def po_count_by_zsite_id(zsite_id):
    return zip(
        PO_CID, _po_count_by_zsite_id(zsite_id)
    )

def feed_po_list_by_zsite_id(user_id, zsite_id, cid, limit, offset):
    return render_zsite_feed_list(
            user_id,
            po_id_list_by_zsite_id(zsite_id, cid, limit, offset)
        )

@mc_po_id_list_by_zsite_id('{zsite_id}_{cid}')
def po_id_list_by_zsite_id(zsite_id, cid, limit, offset):
    qs = Po.where(
        zsite_id=zsite_id
    ).where('state>=%s'%STATE_PO_ZSITE_SHOW_THEN_REVIEW)

    if cid:
        qs = qs.where(cid=cid)

    return qs.order_by('id desc').col_list(limit, offset)

def po_list_by_zsite_id(zsite_id, cid , limit, offset):
    return Po.mc_get_list(po_id_list_by_zsite_id(
        zsite_id, cid , limit, offset
    ))


def mc_flush_zsite_cid(zsite_id, cid):
    if zsite_id:
        from model.site_po import mc_po_count_by_zsite_id, po_cid_count_by_zsite_id
        po_cid_count_by_zsite_id.delete(zsite_id, cid)
        mc_po_count_by_zsite_id.delete(zsite_id)
        po_cid_count_by_zsite_id.delete(zsite_id, 0)
        mc_po_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, cid))
        mc_po_id_list_by_zsite_id.delete('%s_%s'%(zsite_id, 0))


if __name__ == '__main__':
    print po_id_list_by_zsite_id(10099440, 0, 33, 0)
