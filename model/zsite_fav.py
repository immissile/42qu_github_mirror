#coding:utf-8
from model.zsite_list import zsite_list_new, STATE_DEL, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id
from model.zsite import Zsite
from model.buzz import mq_buzz_site_fav

def zsite_fav_rm(zsite, owner_id):
    zsite_list_rm(
        zsite.id,
        owner_id,
        zsite.cid
    )

def zsite_fav_new(zsite, owner_id):
    zsite_id = zsite.id
    zsite = zsite_list_new(
        zsite_id,
        owner_id,
        zsite.cid,
        1,
        STATE_ACTIVE
    )
    mq_buzz_site_fav(owner_id, zsite_id)


def zsite_fav_touch(zsite, owner_id):
    zsite_list_new(
        zsite.id,
        owner_id,
        zsite.cid,
        1,
        STATE_DEL
    )

def zsite_fav_get(zsite, owner_id):
    return zsite_list_get(
        zsite.id,
        owner_id,
        zsite.cid
    )

def zsite_fav_id_get(zsite, owner_id):
    return zsite_list_id_get(
        zsite.id,
        owner_id,
        zsite.cid
    )

def zsite_fav_list(zsite, limit, offset):
    id_list = zsite_id_list_by_zsite_id(
        zsite.id,
        zsite.cid,
        limit,
        offset
    )
    return Zsite.mc_get_list(id_list)

def zsite_fav_get_and_touch(zsite, owner_id):
    id , state = zsite_list_id_state(zsite.id, owner_id, zsite.cid)
    if id:
        ZsiteList.raw_sql("update zsite_list set rank=rank+1 where id=%s", id)
        return id
    else:
        zsite_fav_touch(zsite, owner_id)   

def zsite_fav_count_by_zsite(zsite):
    return zsite_list_count_by_zsite_id(
        zsite.id, zsite.cid
    )
