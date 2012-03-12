#coding:utf-8
from model.po import Po
from model.zsite import Zsite
from model.txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow
from model.fav import fav_cid_dict

def po_json(user_id, po_id_list, line_width):

    po_id_list = map(int,po_id_list)

    po_list = Po.mc_get_list(po_id_list)

    txt_bind(po_list)

    Zsite.mc_bind(po_list, 'user', 'user_id')
    result = []


    fav_dict = fav_cid_dict(
        user_id,
        po_id_list
    )

    for po in po_list:

        name = po.name
        user = po.user


        name_len = cnenlen(name)
        txt = po.txt

        if txt and name_len < line_width:
            tip = cnenoverflow(txt, line_width-name_len)[0]
        else:
            tip = ''

        id = po.id
        if not user:
            user_id = 0
            user_name = None
        else:
            user_id = user.id
            user_name = None
        result.append((
            id,
            name,
            tip,
#            user_id,
#            user_name,
            fav_dict[id]
        ))
# 0   1       2     3           4               5
# id , name, tip,  author_id , author_name , is_star 
    return result

if __name__ == "__main__":
    pass



