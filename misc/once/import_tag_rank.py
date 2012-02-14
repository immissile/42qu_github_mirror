#coding:utf-8
import _env
from misc.spider.zhihu_topic_id_rank import ID2RANK
from zweb.orm import ormiter
from model.cid import CID_TAG
from model.zsite import Zsite
from model.zsite_list import zsite_list_new

for i in ormiter(Zsite,"cid=%s"%CID_TAG):
    id = i.id
    rank = ID2RANK.get(id, 0) 
    print id, rank
    zsite_list_new(id, 0, CID_TAG, rank)

if __name__ == "__main__":
    pass



