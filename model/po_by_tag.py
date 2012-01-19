#coding:utf-8
import _db
from model.po import Po
from model.cid import CID_NOTE
from model.zsite import Zsite
from model.txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow
from model.fav import fav_cid_dict
from _db import  McModel,McLimitA

class PoZsiteTag(McModel):
    pass

mc_po_id_list = McLimitA('PoZsiteTag.%s', 512)

@mc_po_id_list('{tag_id}')
def po_id_list(tag_id,limit,offset):
    po_list =  PoZsiteTag.where(zsite_id=tag_id).order_by('rank desc').col_list(limit, offset)
    return po_list

def po_by_tag(tag_id, user_id):
    po_list = Po.where(cid=CID_NOTE).order_by('id desc')[:25]
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

if __name__ == '__main__':
    pass
    #print po_by_tag(1, 0)
    print po_id_list(tag_id=1,limit=100,offset=0,)
