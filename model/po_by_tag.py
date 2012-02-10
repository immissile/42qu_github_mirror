#coding:utf-8
from _db import  McModel, McLimitA, McNum
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

class PoZsiteTag(McModel):
    pass

def zsite_tag_po_new(zsite_id, po, rank):
    tag_po = PoZsiteTag.get_or_create(po_id=po.id, cid=po.cid, zsite_id=zsite_id)
    tag_po.rank=rank
    tag_po.save()

    user_rank = zsite_list_get(po.user_id, zsite_id, CID_TAG)
    if not user_rank:
        user_rank = zsite_list_new(po.user_id, zsite_id, CID_TAG)
    else:
        user_rank.rank += 1
        user_rank.save()

    mc_flush(zsite_id)

    return tag_po

zsite_tag_po_count=McNum(
    lambda tag_id: PoZsiteTag.where(zsite_id=tag_id).count(),
    "ZsiteTagPoCount:%s"
)
def mc_flush(zsite_id):
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
    zsite_list = filter(lambda x:x,zsite_author_list(zsite_id))
    return zsite_json(zsite_id, zsite_list)

def zsite_tag_po_new_by_name(tag_name,po,rank):
    tag_name=tag_name.strip()
    tag = tag_by_name(tag_name)
    return zsite_tag_po_new(tag.id, po, rank)

def tag_po_rm_by_po_id(po_id):
    for tag in PoZsiteTag.where(po_id=po_id):
        tag.delete()
        mc_flush(tag.zsite_id)

def tag_list_by_po_id(po_id):
    zsite_id_list = PoZsiteTag.where(po_id=po_id).col_list(col="zsite_id")
    return Zsite.mc_get_list(zsite_id_list)

def po_id_tag_id_list_new(po, tag_id_list):
    pass
    #tag_po_rm_by_po_id(po.id)

    #tag_id_list = tag_id_list.split(',')
    #for tag in tag_id_list:
    #    zsite_tag_po_new_by_name(tag, po, 100)

    #tag_id_list = feed.tag_id_list.split(' '
    #rec_read_new(po.id, tag_id_list)

if __name__ == '__main__':
    pass
    print tag_list_by_po_id(69217)
    #print po_by_tag(1, 0)
