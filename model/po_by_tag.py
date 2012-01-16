#coding:utf-8
import _db
from model.po import Po
from model.cid import CID_NOTE
from model.zsite import Zsite
from model.txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow

# id , name, txt,  author_id , author_name , is_star 
def po_by_tag(tag_id):
    po_list = Po.where(cid=CID_NOTE)[:25]
    txt_bind(po_list)

    Zsite.mc_bind(po_list, 'user', 'user_id')
    result = []


    for po in po_list:

        name = po.name
        user = po.user


        name_len = cnenlen(name)
        txt = po.txt

        if txt and name_len < 38:
            tip = cnenoverflow(txt, 38-name_len)[0]
        else:
            tip = ''

        result.append((
            po.id,
            name,
            tip,
            user.id,
            user.name
        ))

    return result

if __name__ == '__main__':
    print po_by_tag(1)



