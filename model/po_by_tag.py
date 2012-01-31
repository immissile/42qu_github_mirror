#coding:utf-8
import _db
from model.cid import CID_NOTE
from model.po_json import po_json, Po

def po_by_tag(tag_id, user_id, limit=25):
    id_list = Po.where(cid=CID_NOTE).order_by('id desc').col_list(limit, 0)
    return po_json(user_id, id_list, 36)


if __name__ == '__main__':
    print po_by_tag(1, 0)



