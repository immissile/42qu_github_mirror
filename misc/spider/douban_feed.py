#coding:utf-8

import _env
from model.douban import DoubanRec, DOUBAN_REC_CID
from zweb.orm import ormiter
from douban_parse import DOUBAN_REC_PARSE 
from itertools import chain

def main():
    for cid, func in DOUBAN_REC_PARSE.iteritems():
        for i in ormiter(DoubanRec, 'cid=%s'%cid):
            print func(i.htm, i.user_id)

if __name__ == '__main__':

    main()
