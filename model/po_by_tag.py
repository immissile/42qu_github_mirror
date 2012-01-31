#coding:utf-8
import _db
from po import Po
from cid import CID_NOTE, CID_TAG, CID_USER
from zsite import Zsite
from model.ico import ico_url_bind
from txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow
from fav import fav_cid_dict
from model.motto import motto
from model.follow import follow_get_list
from model.career import career_bind
from _db import  McModel, McLimitA
from zsite_list  import zsite_list_new, zsite_list_get, zsite_id_list

mc_po_id_list = McLimitA('PoZsiteTag.%s', 512)

class PoZsiteTag(McModel):
    pass

def zsite_tag_new_po(po, rank, zsite_id):
    tag_po = PoZsiteTag(po_id=po.id, cid=po.cid, zsite_id=zsite_id, rank=rank)
    tag_po.save()

    author_list = zsite_list_get(po.user_id, zsite_id)
    if not author_list:
        author_list = zsite_list_new(po.user_id, zsite_id, CID_TAG)
    else:
        print '!'
        author_list.rank += 1
        author_list.save()

    return tag_po

def zsite_tag_po_count(tag_id): return PoZsiteTag.where(zsite_id=tag_id).count()

def zsite_author_list(zsite_id):
    return Zsite.mc_get_list(zsite_id_list(zsite_id, CID_TAG))

def get_or_create_tag(tag):
    found = Zsite.get(name=tag, cid=CID_TAG)
    if not found:
        found = zsite_new(k, CID_TAG, ZSITE_STATE_SITE_PUBLIC)
    return found

@mc_po_id_list('{tag_id}-{limit}-{offset}')
def get_po_id_list(tag_id, limit, offset):
    po_list = PoZsiteTag.where(zsite_id=tag_id).order_by('rank desc').col_list(limit, offset, col='po_id')
    return po_list

def po_by_tag(tag_id, user_id, limit, offset):
    po_list = Po.mc_get_list(get_po_id_list(tag_id, limit, offset))
    #po_list = Po.where(cid=CID_NOTE).order_by('id desc')[:25]
    txt_bind(po_list)

    Zsite.mc_bind(po_list, 'user', 'user_id')
    result = []

    po_id_list = [i.id for i in po_list]

    fav_dict = fav_cid_dict(
        user_id,
        po_id_list
    )

    for po in po_list:

        name = po.name
        user = po.user


        name_len = cnenlen(name)
        txt = po.txt

        if txt and name_len < 36:
            tip = cnenoverflow(txt, 36-name_len)[0]
        else:
            tip = ''

        id = po.id

        result.append((
            id,
            name,
            tip,
            user.id,
            user.name,
            fav_dict[id]
        ))
# 0   1       2     3           4               5
# id , name, tip,  author_id , author_name , is_star 
    return result

def tag_author_list(zsite_id):
    zsite_list = zsite_author_list(zsite_id)
    ico_url_bind(zsite_list)
    zsite_id_list = tuple(i.id for i in zsite_list)

    user_list = []
    for i in zsite_list:
        if i.cid == CID_USER:
            user_list.append(i)
    career_bind(user_list)
    motto_dict = motto.get_dict(zsite_id_list)

    result = []

    for i, is_follow in zip(
        zsite_list,
        follow_get_list(zsite_id, zsite_id_list)
    ):
        career = (' , '.join(filter(bool, i.career)) if i.cid==CID_USER else 0) or 0
        _motto = motto_dict.get(i.id) or 0
        if _motto:
            length = 14
            if not career:
                length += length
            _motto = cnenoverflow(_motto, length)[0]

        if is_follow and is_follow is not True:
            is_follow = 1
        result.append((
            i.id, #0 
            i.link, #1
            i.name, #2
            i.ico, #3
            career, #4
            i.cid , #5
            _motto , #6
            is_follow , #7
        ))
    return result


if __name__ == '__main__':
    pass
    #print po_by_tag(1, 0)
    for i in  get_po_id_list(tag_id=61662, limit=100, offset=0, ):
        print i
    print zsite_tag_po_count(61662)
