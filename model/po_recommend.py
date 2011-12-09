#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import cursor_by_table, McModel, McLimitA, McCache, McNum, McCacheA
from state import STATE_RM, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from po import po_new, Po, STATE_ACTIVE, STATE_SECRET, po_list_count
from state import STATE_PO_ZSITE_SHOW_THEN_REVIEW
from model.zsite import Zsite
from model.po import po_rm,reply_rm_if_can
from model.rec2rep import RecRep
from model.reply import Reply
from cid import CID_REC

mc_po_recommend_id_get = McCache('PoRecommendIdGet:%s')
mc_po_rec2rep_get = McCache('PoRecommendIdGet:%s_%s')

def po_recommend_get(rid, user_id):
    id = po_recommend_id_get(rid, user_id)
    return id and Po.mc_get(id)

def po_recommend_new(rid, user_id, name, reply_id=None):
    pre_po = Po.mc_get(rid)

    if pre_po.can_admin(user_id):
        state = STATE_ACTIVE
    else:
        state = STATE_PO_ZSITE_SHOW_THEN_REVIEW

    recommend = po_new(
        CID_REC,
        user_id,
        name,
        state=state,
        rid=rid
    )
    mc_po_recommend_id_get.set(
        '%s_%s'%(rid, user_id),
        recommend.id
    )
    recommend.feed_new()

    if reply_id:
        link = RecRep(
                id=recommend.id,
                reply_id=reply_id)
        link.save()
    return recommend


@mc_po_rec2rep_get('%s_%s')
def get_recommend_to_reply(po_id, reply_id):
    link = RecRep.raw_sql(
            'select id from rec_rep where id=%s and reply_id=%s ',po_id,reply_id)
    r = link.fetchone()
    if r:
        return r[0]
    return None


def po_recommend_get_linked_reply(id):
    """获取连接到推荐po的评论"""
    repl = RecRep.mc_get(id)
    if repl:
        return repl
    return None

def po_recommend_rm_reply(id, user_id):
    '''同步删除评论'''
    linked_reply = po_recommend_get_linked_reply(id)
    if linked_reply:
        reply_rm_if_can(user_id, linked_reply.reply_id)

def _po_recommend_rm(rid, user_id):
    id = po_recommend_id_get(rid, user_id)
    if id:
        po_rm(user_id, id)
        linked_reply = po_recommend_get_linked_reply(id)
        if linked_reply:
            reply_rm_if_can(user_id, linked_reply.reply_id)
            key = '%s_%s'%(rid,user_id)
            mc_po_recommend_id_get.delete(key)

@mc_po_recommend_id_get('{rid}_{user_id}')
def po_recommend_id_get(rid, user_id):
    c = Po.raw_sql(
'select id from po where rid=%s and user_id=%s and cid=%s and state = %s',
rid, user_id, CID_REC, STATE_ACTIVE
    )
    r = c.fetchone()
    if r:
        return r[0]
    return 0

if __name__ == '__main__':
    #po_review_show_id_list_new(1, 2)
    #print po_review_show_id_list(1)
    #name = "gw"
    #po_review_new(zsite_id, user_id, name)

    #po_recommend_new(1055, 10002411, 'SHIT', True)
    #print Po.where(id= po_recommend_id_get(0,10002411))[0]
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

