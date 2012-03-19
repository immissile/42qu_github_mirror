#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.po import po_new, Po, STATE_ACTIVE, STATE_SECRET
from model.cid import CID_REC
from zweb.orm import ormiter
from model.po_recommend import mc_po_recommend_id_by_rid_user_id,RecRep
from model.feed import Feed



def main():
    for vote in ormiter(Feed,'rid !=0'):
        recommend = po_new(
            CID_REC,
            vote.zsite_id,
            '',
            state=STATE_ACTIVE,
            rid=vote.rid,
            id=vote.id
        )
        if recommend:
            mc_po_recommend_id_by_rid_user_id.set(
                '%s_%s'%(vote.rid, vote.zsite_id),
                recommend.id
            )
            vote.cid  =CID_REC
            vote.rid = 0
            vote.save()

if __name__ == '__main__':
    main()
