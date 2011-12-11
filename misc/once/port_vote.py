#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.vote import Vote
from model.po import po_new, Po, STATE_ACTIVE, STATE_SECRET, po_list_count
from model.rec2rep import RecRep
from model.cid import CID_REC
from model.po_recommend import mc_po_recommend_id_by_rid_user_id

def po_recommend_new(rid, user_id, name, reply_id=None):
    '''新建推荐'''
    #判定?
    #rec_po = Po.mc_get(rid)

    recommend = po_new(
        CID_REC,
        user_id,
        name,
        state=STATE_ACTIVE,
        rid=rid
    )

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

def main():
    votes=Vote.where()
    for vote in votes:
        new_rec = po_recommend_new(vote.po_id,vote.user_id,'')

if __name__ == '__main__':
    main()
