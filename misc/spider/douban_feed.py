#coding:utf-8


import _env
from model.douban import DoubanRec, DOUBAN_REC_CID
from zweb.orm import ormiter

def main():
    for rec_name in ('note', 'topic'):
        cid = DOUBAN_REC_CID[rec_name]
        for i in ormiter(DoubanRec, 'cid=%s'%cid):
            print i.id

if __name__ == '__main__':

    main()
