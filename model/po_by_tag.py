#coding:utf-8
from _db import  McModel, McLimitA, McNum, McCacheA
from model.po_json import po_json, Po
from po import Po
from cid import CID_NOTE, CID_TAG, CID_USER
from zsite import Zsite , zsite_new
from model.ico import ico_url_bind
from txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow
from fav import fav_cid_dict
from model.motto import motto
from model.follow import follow_get_list
from model.career import career_bind
from zsite_list  import zsite_list_new, zsite_list_get, zsite_id_list
from zsite_json import zsite_json


mc_po_id_list_by_tag_id = McLimitA('PoIdListByTagId.%s', 512)
mc_tag_id_list_by_po_id = McCacheA("TagIdListByPoId.%s")

class PoZsiteTag(McModel):
    pass

def zsite_tag_po_new(zsite_id, po, rank=1):
    po_id = po.id

    tag_po = PoZsiteTag.get_or_create(po_id=po_id, cid=po.cid, zsite_id=zsite_id)
    tag_po.rank = rank
    tag_po.save()

    user_rank = zsite_list_get(po.user_id, zsite_id, CID_TAG)
    if not user_rank:
        user_rank = zsite_list_new(po.user_id, zsite_id, CID_TAG)
    else:
        user_rank.rank += 1
        user_rank.save()

    mc_flush(zsite_id, po_id)

    return tag_po

zsite_tag_po_count = McNum(
    lambda tag_id: PoZsiteTag.where(zsite_id=tag_id).count(),
    'ZsiteTagPoCount:%s'
)

def mc_flush(zsite_id, po_id):
    mc_flush_by_zsite_id(zsite_id)
    mc_flush_by_po_id(po_id)

def mc_flush_by_zsite_id(zsite_id):
    zsite_tag_po_count.delete(zsite_id)
    mc_po_id_list_by_tag_id.delete(zsite_id)

def zsite_author_list(zsite_id):
    return Zsite.mc_get_list(zsite_id_list(zsite_id, CID_TAG))

def tag_by_name(name):
    found = Zsite.get(name=name, cid=CID_TAG)
    if not found:
        found = zsite_new(name, CID_TAG)
    return found

@mc_po_id_list_by_tag_id('{tag_id}')
def po_id_list_by_tag_id(tag_id, limit, offset=0):
    po_list = PoZsiteTag.where(zsite_id=tag_id).order_by('rank desc').col_list(limit, offset, col='po_id')
    return po_list


def po_by_tag(tag_id, user_id, limit=25, offset=0):
    id_list = po_id_list_by_tag_id(tag_id, limit, offset)
    return po_json(user_id, id_list, 36)

def tag_author_list(zsite_id):
    zsite_list = filter(lambda x:x, zsite_author_list(zsite_id))
    return zsite_json(zsite_id, zsite_list)

def zsite_tag_po_new_by_name(tag_name, po, rank):
    tag_name = tag_name.strip()
    tag = tag_by_name(tag_name)
    return zsite_tag_po_new(tag.id, po, rank)

def tag_rm_by_po_id(po_id):
    for tag_id in tag_id_list_by_po_id(po_id):
        PoZsiteTag.where(zsite_id=tag_id).delete()
        mc_flush_by_zsite_id(tag_id)
    mc_flush_by_po_id(po_id)

@mc_tag_id_list_by_po_id("{po_id}")
def tag_id_list_by_po_id(po_id):
    zsite_id_list = PoZsiteTag.where(po_id=po_id).col_list(col='zsite_id')
    return zsite_id_list(po_id) 

def mc_flush_by_po_id(po_id):
    mc_tag_id_list_by_po_id.delete(po_id)

def tag_list_by_po_id(po_id):
    zsite_id_list = tag_id_list_by_po_id(po_id)
    return Zsite.mc_get_list(zsite_id_list)

def po_tag_id_list_new(po_id, tag_id_list):
    new_tag_id_list = set(map(int, tag_id_list))
    old_tag_id_list = set(tag_id_list_by_po_id)
    
    to_add = new_tag_id_list - old_tag_id_list
    to_rm = old_tag_id_list - new_tag_id_list


    for tag_id in to_rm:
        PoZsiteTag.where(zsite_id=tag_id).delete()
        mc_flush_by_zsite_id(tag_id)
    
    for tag_id in to_add:
        zsite_tag_po_new(zsite_id, po)



    #tag_rm_by_po_id(po.id)

    #tag_id_list = tag_id_list.split(',')
    #for tag in tag_id_list:
    #    zsite_tag_po_new_by_name(tag, po, 100)

    #tag_id_list = feed.tag_id_list.split(' '
    #rec_read_new(po.id, tag_id_list)

if __name__ == '__main__':
    pass
    print tag_list_by_po_id(69217)
    #print po_by_tag(1, 0)
