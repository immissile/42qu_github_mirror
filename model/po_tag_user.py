#coding:utf-8
from _db import  McModel, Model, McNum, McCacheA, redis
from model.tag_id_list import Tag2IdList
from model.zsite import Zsite
from operator import itemgetter
from model.po_tag import po_tag_new_by_autocompelte
from model.po_show import po_show_new

tag2idlist_po_user = Tag2IdList('PoUser')
tag2idlist_po = Tag2IdList('Po')
#tag2idlist_user_rss_po = Tag2IdList('UserRssPo')
REDIS_USER_RSS_PO = "UserRssPo:%s"

def po_pass(user_id, po_id):
    rss_po_pop(user_id, po_id)
#    print user_id, po_id

def po_tag(user_id, po_id, title, txt, sync, tag_id_list, cid):
    #print id, title, txt, sync, tag_id_list, cid
    #pass
    from model.po import Po
    po = Po.mc_get(po_id)
    if po:
        po_tag_new_by_autocompelte(po, tag_id_list, cid)
        po.name_ =  title
        po.save()
        po.txt_set(txt)
        if sync:
            po_show_new(po)

    rss_po_pop(user_id, po_id)

def po_rm(user_id, po_id):
    from model.po import po_rm as _po_rm
    rss_po_pop(user_id, po_id)
    _po_rm(user_id, po_id)

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


def rss_po_pop(user_id, id):
    tag2idlist_po.pop_id(id)
    key = REDIS_USER_RSS_PO%user_id
    redis.lrem(key, id)

def po_id_next_by_user(user_id, offset):
    from model.po import Po
    from model.rss import RssPoId
    id = redis.lindex(REDIS_USER_RSS_PO%user_id, offset)
    if id: 
        po = Po.mc_get(id)
        if po:
            rss_po_id =  RssPoId.get(po_id=id)
            if rss_po_id:
                tag_id_list = rss_po_id.tag_id_list
            else:
                tag_id_list = ""
            tag_id_list = filter(bool, tag_id_list.split(' '))
            tag_id_list = list(
                zip(
                    [ i.name for i in Zsite.mc_get_list(tag_id_list) if i is not None],
                    tag_id_list
                )
            )
            po.tag_id_list = tag_id_list
            return po
 

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
