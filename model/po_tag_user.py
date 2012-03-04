#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis
from model.tag_id_list import Tag2IdList
from model.zsite import Zsite
from operator import itemgetter

tag2idlist_po_user = Tag2IdList('PoUser')
tag2idlist_po = Tag2IdList('Po')
#tag2idlist_user_rss_po = Tag2IdList('UserRssPo')
REDIS_USER_RSS_PO = "UserRssPo:%s"

def rss_po_new(po, user_tag_id_list):
    id = po.id
    tag2idlist_po.append_id_tag_id_list(
        id , user_tag_id_list
    )
    key = REDIS_USER_RSS_PO%po.user_id

    p = redis.pipeline()
    p.lrem(key, id)
    p.rpush(key, id)
    p.execute()

def tag_list_by_user_id(user_id):
    tag_id_list = tag2idlist_po_user.tag_id_list_by_id(user_id)
    tag_list = Zsite.mc_get_list(tag_id_list)
    return tag_list


def tag_list_with_user_count_po_count():
    id_count_list = tag2idlist_po_user.tag_id_count_list()
    po_count_dict = dict(tag2idlist_po.tag_id_count_list())
    id_list = map(itemgetter(0), id_count_list)
    tag_list = Zsite.mc_get_list(id_list)
    for id, tag, count in zip(id_list, tag_list, map(itemgetter(1), id_count_list)):
        tag.user_count = count
        tag.po_count = po_count_dict.get(id,0)
    return tag_list

def user_list_by_tag_id(tag_id):
    user_id_list = tag2idlist_po_user.id_list_by_tag_id(tag_id)
    user_list = Zsite.mc_get_list(user_id_list)
    for i in user_list:
        i.po_count = redis.llen(REDIS_USER_RSS_PO%i.id)
    return user_list


if __name__ == '__main__':
    pass
    print tag2idlist_po.tag_id_count_list()
#tag2idlist_po = Tag2IdList('Po')
#tag2idlist_user_rss_po = Tag2IdList('UserRssPo')


#    from model.rss import Rss, RssPo, RssPoId
#    for i in tag_list_with_user_count():
#        print i.name
#
#        for j in user_list_by_tag_id(i.id):
#            #for l in RssPo.where(user_id=j.id):
#            #    if RssPoId.get(rss_po_id=l.id) or RssPoId.get(l.id):
#            #        print l.title
#            #    else:
#            #        l.delete()
#
#            print '\t', j.name
#            for k in Rss.where(user_id=j.id):
#                #k.gid = 0
#                #k.save()
#
#                #from zkit.google.findrss import get_rss_link_title_by_url
#                #print get_rss_link_title_by_url(k.url)
#                #print all((k.link, k.url, k.name))
#                print '\t\t', k.link, k.url, k.name, k.gid, k.auto
#
#
#
