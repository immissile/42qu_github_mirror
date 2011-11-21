#coding:utf-8

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from po import po_new, Po, STATE_ACTIVE, STATE_SECRET
from cid import CID_REVIEW
from kv import Kv
from array import array

po_review_show = Kv('po_review_show', '')

mc_po_review_id_get = McCache("PoReviewIdGet:%s")

def po_review_new(zsite_id, user_id, name):
    if zsite_member_can_admin(zsite_id, user_id):
        state = STATE_SECRET
    else:
        state = STATE_ACTIVE

    review = po_review_get(zsite_id,user_id)
    if review:
        review.rid = rid
        review.state = state
        review.name = name
        review.save() 
    else:
        review = po_new(
            CID_REVIEW,
            user_id,
            name,
            state=state,
            zsite_id=zsite_id
        )
        mc_po_review_id_get.set(
            "%s_%s"%(zsite_id, user_id),
            review.id
        )

    return review

def po_review_rm(zsite_id, user_id):
    id = po_review_id_get(zsite_id, user_id)
    if id:
        po_rm(user_id, id)

    

@mc_po_review_id_get("{zsite_id}_{user_id}")
def po_review_id_get(zsite_id, user_id):
    c = Po.raw_sql(
"select id from po where zsite_id=%s and user_id=%s and cid=%s",
zsite_id, user_id, CID_REVIEW
    )
    r = c.fetchone()
    if r:
        return r[0]
    return 0


def po_review_get(zsite_id, user_id):
    id = po_review_id_get(zsite_id, user_id)
    return id and Po.mc_get(id)

def po_review_state_set(zsite_id, user_id, rid):
    review = po_review_get(zsite_id, user_id)
    if review:
        review.state = STATE_SECRET if rid else STATE_ACTIVE
        review.save()

def po_review_show_id_list(id):
    a = array('I')
    a.fromstring(po_review_show.get(id)) 
    return a 

def po_review_show_id_list_new(id, po_id):
    id_list = po_review_show_id_list(id)
    if po_id not in id_list:
        id_list.append(po_id)
    po_review_show.set(id, id_list.tostring())

if __name__ == "__main__":
    po_review_show_id_list_new(1, 2)
    print po_review_show_id_list(1)

