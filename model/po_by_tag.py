#coding:utf-8
from model.po import Po
from model.cid import CID_NOTE

# id , name, txt,  author_id , author_name , is_star 
def po_by_tag(tag_id):
    po_list = Po.where(cid=CID_NOTE)[:25]
    result = []
    for po in po_list:
        result.append((
            po.id, 
            po.name, 
            po.txt,
            po.user_id
        ))
    return result

if __name__ == "__main__":
    pass



