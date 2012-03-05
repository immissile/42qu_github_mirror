#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis
from model.tag_id_list import Tag2IdList
from model.zsite import Zsite


tag2idlist_po_user = Tag2IdList('PoUser')
tag2idlist_po = Tag2IdList('Po')

def tag_list_by_user_id(user_id):
    tag_id_list = tag2idlist_po_user.tag_id_list_by_id(user_id)
    tag_list = Zsite.mc_get_list(tag_id_list)
    return tag_list



if __name__ == '__main__':
    pass

    for i in tag_list_by_user_id(10000000):
        print i


