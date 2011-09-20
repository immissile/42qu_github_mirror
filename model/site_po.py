#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, Model, McCacheM
from po import Po
from model.state import STATE_PO_ZSITE_REVIEW , STATE_PO_ZSITE_ACCPET 


mc_pos_id_list_by_cid = McCacheM("PosIdListByCid:%s")


def po_list_by_zsite_id(zsite_id, cid, limit, offset):
    return Po.mc_get_list(
        po_id_list_by_zsite_id(zsite_id, cid,  limit, offset)
    )

def po_id_list_by_zsite_id(zsite_id, cid,  limit, offset):

    qs = Po.where(
        zsite=zsite_id, cid=cid
    ).where("state>=%s"%STATE_PO_ZSITE_ACCPET)
 
    return qs.order_by('id desc').col_list(limit, offset)

class ZsiteSiteMax(Model):
    pass

class ZsiteSitePos(Model):
    pass


def pos_id_list_by_cid(zsite_id , user_id):
    r = ZsiteSitePos.where(zsite_id=zsite_id, user_id=user_id).col_list(
            col='cid,pos_id'
        )
    return dict(r)

def pos_mark_all(zsite_id, user_id):
    pass

def pos_mark(zsite_id, user_id, cid):
    pass

def next_id_list(zsite_id, user_id):
    pass


if __name__ == "__main__":
    print pos_id_list_by_cid(1, 2)

