#coding:utf-8
from _db import McLimitA
from zsite_list import ZsiteList
from zsite import Zsite

ZSITE_LIST_0_CID = (
    (1, '创业'),
    (2, '程序'),
    (3, '设计'),
    (4, '产品'),
    (5, '运营'),
    (6, '文化'),
    (7, '媒体'),
    (8, '金融'),
    (9, '商务'),
    (10, '管理'),
    (11, '公关'),
    (12, '科研'),
    (13, '健康'),
)

mc_reply_id_list = McLimitA("ZsiteListId0:%s", 1024)

@mc_reply_id_list("{cid}")
def zsite_list_id_0(cid=0, limit=None, offset=None):
    zsite_list = ZsiteList.where().order_by("rank desc")
    if cid:
        zsite_list = zsite_list.where(cid=cid)
    return zsite_list.id_list(limit, offset)

def zsite_list_new(zsite_id, cid, rank=1000):
    zsite = ZsiteList.get_or_create(
        zsite_id=zsite_id, owner_id=owner_id, cid=0, rank=rank
    )
    zsite.rank = rank
    zsite.save()

def zsite_list_get(zsite_id):
    return ZsiteList.get(zsite_id=zsite_id, owner_id=0)

if __name__ == "__main__":
    print zsite_list_id_0()

