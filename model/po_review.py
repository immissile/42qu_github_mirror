#coding:utf-8

from _db import cursor_by_table, McModel, McCache, McNum, McCacheA
from po import po_new, Po, STATE_ACTIVE
from cid import CID_REVIEW
from kv import Kv
from array import array
from model.site_po import po_cid_count_by_zsite_id, po_list_by_zsite_id
from state import STATE_PO_ZSITE_SHOW_THEN_REVIEW
from career import career_bind
from model.zsite import Zsite

po_review_show = Kv('po_review_show', '')

mc_po_review_id_get = McCache('PoReviewIdGet:%s')

def po_review_new(zsite_id, user_id, name):
    from model.zsite_member import zsite_member_can_admin
    if zsite_member_can_admin(zsite_id, user_id):
        state = STATE_ACTIVE
    else:
        state = STATE_PO_ZSITE_SHOW_THEN_REVIEW

    review = po_review_get(zsite_id, user_id)

    if review:
        if not name:
            po_review_rm(zsite_id, user_id)
        else:
            review.state = state
            review.name_ = name
            review.save()
    else:
        review = po_new(
            CID_REVIEW,
            user_id,
            name,
            state=state,
            zsite_id=zsite_id
        )
        if review:
            mc_po_review_id_get.set(
                '%s_%s'%(zsite_id, user_id),
                review.id
            )
            review.feed_new()

    if state == STATE_ACTIVE:
        mc_po_review_id_list_active_by_zsite_id.delete(zsite_id)
    return review


def po_review_rm(zsite_id, user_id):
    id = po_review_id_get(zsite_id, user_id)
    if id:
        po_rm(user_id, id)



@mc_po_review_id_get('{zsite_id}_{user_id}')
def po_review_id_get(zsite_id, user_id):
    c = Po.raw_sql(
'select id from po where zsite_id=%s and user_id=%s and cid=%s',
zsite_id, user_id, CID_REVIEW
    )
    r = c.fetchone()
    if r:
        return r[0]
    return 0

def po_review_count(zsite_id):
    return po_cid_count_by_zsite_id(zsite_id, CID_REVIEW)

def po_review_list_by_zsite_id(zsite_id, limit, offset):
    review_list = po_list_by_zsite_id(zsite_id, CID_REVIEW , limit, offset)
    po_review_bind(review_list)
    return review_list

def po_review_get(zsite_id, user_id):
    id = po_review_id_get(zsite_id, user_id)
    return id and Po.mc_get(id)

def po_review_state_set(zsite_id, user_id, rid):
    review = po_review_get(zsite_id, user_id)
    if review:
        review.state = STATE_ACTIVE if rid else STATE_PO_ZSITE_SHOW_THEN_REVIEW
        review.save()
        mc_po_review_id_get.set(
            '%s_%s'%(zsite_id, user_id),
            review.id
        )
        mc_po_review_id_list_active_by_zsite_id.delete(zsite_id)

def po_review_show_id_list(id):
    a = array('I')
    a.fromstring(po_review_show.get(id))
    return a

def po_review_bind(review_list):
    Zsite.mc_bind(review_list, 'user', 'user_id')
    career_bind(i.user for i in review_list)

def po_review_show_list_with_user(id):
    review_list = Po.mc_get_list(po_review_show_id_list(id))
    po_review_bind(review_list)
    return review_list

def po_review_show_new(id, po_id):
    id_list = po_review_show_id_list(id)
    po_id = int(po_id)
    if po_id not in id_list:
        id_list.insert(0, po_id)
    po_review_show.set(id, id_list.tostring())

def po_review_show_rm(id, po_id):
    id_list = po_review_show_id_list(id)
    po_id = int(po_id)
    try:
        id_list.remove(po_id)
    except ValueError:
        pass
    po_review_show.set(id, id_list.tostring())

mc_po_review_id_list_active_by_zsite_id = McCacheA('PoReviewIdListActiveByZsiteId.%s')

@mc_po_review_id_list_active_by_zsite_id('{id}')
def po_review_id_list_active_by_zsite_id(id):
    qs = Po.where(
        zsite_id=id,
        cid=CID_REVIEW
    ).where('state=%s'%STATE_ACTIVE).order_by('id desc')
    return qs.col_list()

def po_review_list_active_by_zsite_id(id):
    return Po.mc_get_list(
        po_review_id_list_active_by_zsite_id(id)
    )


if __name__ == '__main__':
    #po_review_show_id_list_new(1, 2)
    #print po_review_show_id_list(1)
    #name = "gw"
    #po_review_new(zsite_id, user_id, name)
    #print po_review_id_get(895, 893)

#    user_id =893
#    zsite_id = 895
#    for i in po_review_list_active_by_zsite_id(zsite_id):
#        print i.name
    zsite_id = 895

#    print po_review_count(zsite_id)
#    print po_review_list_by_zsite_id(zsite_id, 0, 1111)
    zsite_id = 10163143
    user_id = 10002411
    po_review_get(zsite_id, user_id)

    for i in Po.where(
        zsite_id=zsite_id
    ).where('state=%s'%STATE_ACTIVE).order_by('id desc'):
        print i.user_id, i.state

