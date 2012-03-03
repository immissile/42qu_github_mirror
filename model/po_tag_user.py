#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis
from model.tag_id_list import Tag2IdList
from model.zsite import Zsite
from operator import itemgetter

tag2idlist_po_user = Tag2IdList('PoUser')
tag2idlist_po = Tag2IdList('Po')

def tag_list_by_user_id(user_id):
    tag_id_list = tag2idlist_po_user.tag_id_list_by_id(user_id)
    tag_list = Zsite.mc_get_list(tag_id_list)
    return tag_list


def tag_list_with_user_count():
    id_count_list = tag2idlist_po_user.tag_id_count_list()
    tag_list = Zsite.mc_get_list(map(itemgetter(0), id_count_list))
    for tag, count in zip(tag_list, map(itemgetter(1), id_count_list)):
        tag.user_count = count 
    return tag_list

def user_list_by_tag_id(tag_id):
    user_id_list = tag2idlist_po_user.id_list_by_tag_id(tag_id)
    user_list = Zsite.mc_get_list(user_id_list)
    return user_list


if __name__ == '__main__':
    pass

#    for i in tag_list_by_user_id(10000000):
#        print i
#    print tag2idlist_po_user.tag_id_count_list()
    for i in tag_list_with_user_count():
        print i.name
         
        for j in user_list_by_tag_id(i.id):
            print "\t",j.name
