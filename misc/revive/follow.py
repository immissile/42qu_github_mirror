#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.follow import Follow, CID_MAN
from model.follow import _follow_new
from model.zsite import Zsite
from model.zsite_rank import zsite_rank_by_zsite_id, zsite_rank_update_by_zsite_id

def main():
    for i in Zsite.where().col_list():
        zsite_rank_update_by_zsite_id(
            i,
            zsite_rank_by_zsite_id(i)
        )
        
    for i in Follow.where(cid=CID_MAN):
        _follow_new(i.from_id, i.to_id)


if __name__ == '__main__':
    main()

