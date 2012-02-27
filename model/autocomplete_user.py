#!/usr/bin/env python
# -`- coding: utf-8 -`-

from _db import redis
from model.zsite import Zsite , CID_USER

def name_to_user(user):
    r = []
    user = user.name
    

if __name__ == '__main__':
    pass
    for i in Zsite.where(cid=CID_USER):
        print i.name

