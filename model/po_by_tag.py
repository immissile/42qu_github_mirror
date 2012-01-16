#coding:utf-8
import _db
from model.po import Po
from model.cid import CID_NOTE
from model.zsite import Zsite

# id , name, txt,  author_id , author_name , is_star 
def po_by_tag(tag_id):
    po_list = Po.where(cid=CID_NOTE)[:25]
    Zsite.mc_bind(po_list,"user", "user_id")
    result = []
    for po in po_list:
        user = po.user
        result.append((
            po.id, 
            po.name, 
            po.txt,
            po.user_id
        ))
    return result

if __name__ == "__main__":
    print po_by_tag(1)



