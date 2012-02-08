#coding:utf-8
import _db
from model.zsite_list import zsite_list_new, STATE_RM, STATE_ACTIVE, zsite_list_get, zsite_list_id_get, zsite_list_rm, zsite_list_count_by_zsite_id , zsite_list_id_state, ZsiteList, zsite_id_list_by_zsite_id
from model.zsite import Zsite
from model.buzz import mq_buzz_site_fav
from model.cid import CID_TAG
from model.auto_tag import tag_tag

def zsite_fav_rm(zsite, owner_id):
    fav = zsite_fav_get(zsite, owner_id)
    if fav.state <= STATE_ACTIVE:
        zsite_list_rm(
            zsite.id,
            owner_id,
            zsite.cid
        )

def zsite_fav_new(zsite, owner_id):
    if zsite_fav_get(zsite, owner_id):
        return

    #TODO: 在将标签数据导入redis后使用
    '''
    if zsite.cid == CID_TAG:
        #tag_tag.tag_fav(zsite.cid)
    '''

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
        STATE_RM
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
        ZsiteList.raw_sql('update zsite_list set rank=rank+1 where id=%s', id)
        return id
    else:
        zsite_fav_touch(zsite, owner_id)

def zsite_fav_count_by_zsite(zsite):
    return zsite_list_count_by_zsite_id(
        zsite.id, zsite.cid
    )

def zsite_fav_rm_all_by_zsite_id(zsite_id):
    zsite = Zsite.mc_get(zsite_id)
    fav_list = ZsiteList.where(zsite_id=zsite_id)
    for fav in fav_list:
        zsite_list_rm(
            zsite.id,
            fav.owner_id,
            zsite.cid
        )
        #zsite_fav_rm(zsite,fav.owner_id)

if __name__ == '__main__':
    zsite_fav_rm_all_by_ziste_id(561)
    #from zsite_url import id_by_url
    #zsite_id = id_by_url('dongxi')
    #from model.zsite import Zsite

#
#
#if __name__ == "__main__":
#    z = Zsite.mc_get(561)
#    print zsite_fav_rm_all_by_ziste_id(z)
