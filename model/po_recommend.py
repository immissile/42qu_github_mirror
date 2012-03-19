#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from state import STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from po import po_new, Po, STATE_ACTIVE, po_list_count
from model.po import po_rm, reply_rm_if_can
from model.reply import Reply
from cid import CID_REC

mc_po_recommend_id_by_rid_user_id = McCache('PoRecommendIdByRidUserId:%s')
mc_reply_id_by_recommend = McCache('ReplyIdByRecommend:%s')

class RecRep(McModel):
    pass


def rm_rec_po_by_po_id(user_id,id):
    ''' DANGEROUS USE WITH CAUTION '''
    for po in Po.where('cid = %s and rid=%s',CID_REC,id):
        po_rm(po.user_id,po.id)

from mq import mq_client
mq_rm_rec_po_by_po_id = mq_client(rm_rec_po_by_po_id)

def po_recommend_new(rid, user_id, name, reply_id=None):
    '''新建推荐'''
    #判定?
    rec_po = Po.mc_get(rid)
    if not rec_po:
        return
    from po_pos import po_pos_state_buzz
    po_pos_state_buzz(user_id, rec_po)

    recommend = po_new(
        CID_REC,
        user_id,
        name,
        state=STATE_ACTIVE,
        rid=rid
    )
    if recommend:
        recommend.feed_new()

        mc_po_recommend_id_by_rid_user_id.set(
            '%s_%s'%(rid, user_id),
            recommend.id
        )

        if reply_id:
            rr = RecRep(
                id=recommend.id,
                reply_id=reply_id
            )
            rr.save()


        return recommend


@mc_reply_id_by_recommend('{po_id}_{reply_id}')
def reply_id_by_recommend(po_id, reply_id):
    link = RecRep.raw_sql(
            'select id from rec_rep where id=%s and reply_id=%s ', po_id, reply_id
    )
    r = link.fetchone()
    if r:
        return r[0]
    return 0


def po_recommend_rm_reply(id, user_id):
    '''同步删除评论'''
    linked_reply = RecRep.mc_get(id)
    if linked_reply:
        reply_rm_if_can(user_id, linked_reply.reply_id)

#def _po_recommend_rm(rid, user_id):
#    id = po_recommend_id_by_rid_user_id(rid, user_id)
#    if id:
#        po_rm(user_id, id)
#        linked_reply = RecRep.mc_get(id)
#        if linked_reply:
#            reply_rm_if_can(user_id, linked_reply.reply_id)
#            key = '%s_%s'%(rid, user_id)
#            mc_po_recommend_id_by_rid_user_id.delete(key)

@mc_po_recommend_id_by_rid_user_id('{rid}_{user_id}')
def po_recommend_id_by_rid_user_id(rid, user_id):
    c = Po.raw_sql(
        'select id from po where rid=%s and user_id=%s and cid=%s and state = %s',
        rid, user_id, CID_REC, STATE_ACTIVE
    )
    r = c.fetchone()
    if r:
        return r[0]
    return 0

def po_recommend_by_rid_user_id(rid, user_id):
    id = po_recommend_id_by_rid_user_id(rid, user_id)
    return id and Po.mc_get(id)

if __name__ == '__main__':
    #po_review_show_id_list_new(1, 2)
    #print po_review_show_id_list(1)
    #name = "gw"
    #po_review_new(zsite_id, user_id, name)

    #po_recommend_new(1055, 10002411, 'SHIT', True)
    #print Po.where(id= po_recommend_id_by_rid_user_id(0,10002411))[0]
    _po_recommend_rm(1200, 10071241)

#    user_id =893
#    zsite_id = 895
#    for i in po_review_list_active_by_zsite_id(zsite_id):
#        print i.name
    #zsite_id = 895

#    print po_review_count(zsite_id)
#    print po_review_list_by_zsite_id(zsite_id, 0, 1111)
    #zsite_id = 10163143
    #user_id = 10002411
    #po_review_get(zsite_id, user_id)

    #for i in Po.where(
    #    zsite_id=zsite_id
    #).where('state=%s'%STATE_ACTIVE).order_by('id desc'):
    #    print i.user_id, i.state

