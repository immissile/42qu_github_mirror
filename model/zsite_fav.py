#coding:utf-8
from model.zsite_list import zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id



def zsite_fav_rm(zsite, owner_id):
    zsite_list_rm(
        zsite.id,
        owner_id,
        zsite.cid
    )

def zsite_fav_new(zsite, owner_id):
    zsite = zsite_list_new(
        zsite.id,
        owner_id,
        zsite.cid,
        1,
        STATE_ACTIVE
    )


def zsite_fav_touch(zsite, owner_id):
    zsite_list_new(
        zsite.id,
        owner_id,
        zsite.cid,
        1,
        STATE_DEL
    )


def zsite_fav_id_get(zsite, owner_id):
    return zsite_list_id_get(
        zsite.id,
        owner_id,
        zsite.cid
    )

def zsite_fav_get_and_touch(zsite_id, owner_id):
    r = zsite_fav_get(zsite_id, owner_id)
    if r:
        r.rank+=1
        r.save()
    else:
        zsite_fav_touch(zsite_id, owner_id)   

def zsite_fav_count_by_zsite_id(zsite):
    return zsite_list_count_by_zsite_id(
        zsite.id, zsite.cid
    )
