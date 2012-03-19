#!/usr/bin/env python
# -*- coding: utf-8 -*-


import _env
from model.follow import follow_id_list_by_from_id
from model.zsite import Zsite
from zweb.orm import ormiter
from model.cid import CID_MAIL_DAY, CID_MAIL_MONTH, CID_MAIL_YEAR, CID_BUZZ_FOLLOW, CID_MAIL_WEEK
from collections import defaultdict
import heapq


def handleUser(id):
    friend_rec=defaultdict(list)
    fo_list = follow_id_list_by_from_id(id)
    for friend in fo_list:
        fr_friend = follow_id_list_by_from_id(friend)
        for candi_fri in fr_friend:
            if candi_fri not in fo_list and candi_fri!=id:
                friend_rec[candi_fri].append(friend)
    return sorted(friend_rec.iteritems(),key=lambda x:len(x[1]),reverse=True)[:3]

def main():
    for i in ormiter(Zsite,'cid=%s'%CID_USER):
        pass

if __name__ == '__main__':
    print handleUser(10031395)
