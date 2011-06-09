#coding:utf-8
from _db import McLimitA
from zsite_list import ZsiteList
from zsite import Zsite


mc_reply_id_list = McLimitA('ZsiteListId0:%s', 1024)

@mc_reply_id_list('{cid}')
def zsite_list_id_0(cid=0, limit=None, offset=None):
    zsite_list = ZsiteList.where().order_by('rank desc')
    if cid:
        zsite_list = zsite_list.where(cid=cid)
    return zsite_list.id_list(limit, offset)

def zsite_list_new(zsite_id, cid=0, rank=1000):
    zsite = ZsiteList.get_or_create(
        zsite_id=zsite_id, owner_id=0, cid=cid, rank=rank
    )
    zsite.rank = rank
    zsite.save()
    mc_reply_id_list.delete(cid)

def zsite_list_rm(zsite_id):
    for i in ZsiteList.where(zsite_id=zsite_id, owner_id=0):
        mc_reply_id_list.delete(i.cid)
        i.delete()

def zsite_list_get(zsite_id):
    return ZsiteList.get(zsite_id=zsite_id, owner_id=0)

if __name__ == '__main__':
    print zsite_list_id_0()

