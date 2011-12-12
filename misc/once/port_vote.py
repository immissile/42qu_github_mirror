#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.vote import Vote
from model.po import po_new, Po, STATE_ACTIVE, STATE_SECRET, po_list_count
from model.cid import CID_REC
from zweb.orm import ormiter
from model.po_recommend import mc_po_recommend_id_by_rid_user_id,RecRep
from model.feed import Feed

def po_recommend_new(rid, user_id, name, vote_id): 
    
    recommend = po_new(
        CID_REC,
        user_id,
        name,
        state=STATE_ACTIVE,
        rid=rid,
        id=vote_id
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
    for vote in ormiter(Feed,'rid !=0'):
        po_recommend_new(vote.rid,vote.zsite_id,'',vote.id)

if __name__ == '__main__':
    main()
