#coding:utf-8
from model.zsite_list import zsite_list_new, STATE_DEL

def zsite_fav_new(zsite, owner_id):
    pass


def zsite_fav_touch(zsite, owner_id):
    zsite_list_new(
        zsite.id,
        owner_id
        zsite.cid,
        1,
        STATE_DEL
    )


def zsite_fav_get(zsite_id, owner_id):
    pass

def zsite_fav_get_and_touch(zsite_id, owner_id):
    r = zsite_fav_get(zsite_id, owner_id)
    if r:
        r.rank+=1
        r.save()
    else:
        zsite_fav_touch(zsite_id, owner_id)   

