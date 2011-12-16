#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
friend_rec.py
Author: WooParadog
Email:  Guohaochuan@gmail.com

Created on
2011-12-16
'''

from model.follow import follow_id_list_by_from_id
from zsite import Zsite
from zweb.orm import ormiter
from model.cid import CID_INVITE_QUESTION, CID_MAIL_DAY, CID_MAIL_MONTH, CID_MAIL_YEAR, CID_BUZZ_FOLLOW, CID_MAIL_WEEK
from collections import defaultdict


def handleUser(id):
    friend_rec=defaultdict(list)
    fo_list = follow_id_list_by_from_id(id)
    for friend in fo_list:
        fr_friend = follow_id_list_by_from_id(friend)
        for candi_fri in fr_friend:
            friend_rec[candi_fri].append(fr_friend)
    yield friend_rec()

def main():
    for i in ormiter(Zsite,'cid=%s'%CID_USER):
        pass

if __name__ == '__main__':
    handleUser(10031395)
    #main()
