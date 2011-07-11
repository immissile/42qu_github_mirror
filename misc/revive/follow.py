#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
#from qu.mysite.model.follow import Follow, CID_MAN
from model.follow import _follow_new, Follow
from model.zsite import Zsite
from model.zsite_rank import zsite_rank_by_zsite_id, zsite_rank_update_by_zsite_id

def main():
        #print i, rank
        
#    for i in Follow.where(cid=CID_MAN):
#        if Zsite.mc_get(i.to_id) and Zsite.mc_get(i.from_id):
#            _follow_new(i.from_id, i.to_id)
    Follow.where().delete()
   # for i in Zsite.where().col_list():
   #     rank = zsite_rank_by_zsite_id(i)
   #     zsite_rank_update_by_zsite_id(i, rank)

if __name__ == '__main__':
    main()
    pass

