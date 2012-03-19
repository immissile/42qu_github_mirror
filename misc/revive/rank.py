#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.follow import Follow
from model.follow import Follow
from model.zsite import Zsite
from model.zsite_rank import zsite_rank_by_zsite_id, zsite_rank_update_by_zsite_id

def main():
    for i in Zsite.where().col_list():
        rank = zsite_rank_by_zsite_id(i)
        zsite_rank_update_by_zsite_id(i, rank)

if __name__ == '__main__':
    main()
