#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA
from model.po_json import po_json, Po
from po import Po
from cid import CID_NOTE, CID_TAG, CID_USER
from zsite import Zsite , zsite_new
from model.ico import ico_url_bind
from txt import txt_bind
from zkit.txt import cnenlen , cnenoverflow
from fav import fav_cid_dict
from model.motto import motto
from model.follow import follow_get_list
from model.career import career_bind
from zsite_list  import zsite_list_new, zsite_list_get, zsite_id_list
from zsite_json import zsite_json
from zkit.algorithm.unique import unique
from zkit.pprint import pprint
from zkit.fanjian import utf8_ftoj


mc_po_id_list_by_tag_id = McLimitA('PoIdListByTagId.%s', 512)
mc_tag_id_list_by_po_id = McCacheA('TagIdListByPoId.%s')



class PoZsiteTag(Model):
    pass

def zsite_tag_po_new(zsite_id, po, rank=1):
    po_id = po.id

    tag_po = PoZsiteTag.get_or_create(po_id=po_id, cid=po.cid, zsite_id=zsite_id)
    tag_po.rank = rank
    tag_po.save()

    user_id = po.user_id
    if user_id:
        user_rank = zsite_list_get(user_id, zsite_id, CID_TAG)
        if not user_rank:
            user_rank = zsite_list_new(user_id, zsite_id, CID_TAG)
        else:
            user_rank.rank += 1
            user_rank.save()

    mc_flush(zsite_id, po_id)

    return tag_po

zsite_tag_po_count = McNum(
    lambda tag_id: PoZsiteTag.where(zsite_id=tag_id).count(),
    'ZsiteTagPoCount:%s'
)

def mc_flush(zsite_id, po_id):
    mc_flush_by_zsite_id(zsite_id)
    mc_flush_by_po_id(po_id)

def mc_flush_by_zsite_id(zsite_id):
    zsite_tag_po_count.delete(zsite_id)
    mc_po_id_list_by_tag_id.delete(zsite_id)

def zsite_author_list(zsite_id):
    return Zsite.mc_get_list(zsite_id_list(zsite_id, CID_TAG))


def tag_rename(id, name):
    # zsite.name 豆瓣 - > 豆瓣 / douban
    pass

def tag_new(name):
    found = Zsite.get(name=name, cid=CID_TAG)
    if not found:
        found = zsite_new(name, CID_TAG)
    #TODO
    #1. 更新autocompelete
    #2. 更新别名库
    
    id = None
    return id 

def tag_by_name(name):
    low = name.lower()
    #TODO
    #查找别名库
    id = None
    if not id:
        id = tag_new(name)
    return id

def tag_alias_new(id, name):
    #添加别名
    pass

def tag_alias_rm(id, name):
    pass

def tag_alias_by_id(id):
    pass

def tag_alias_by_id_str(id, name):
    #根据 id 和 name 返回别名 (自动补全提示的时候, 如果输入的字符串 lower以后不在tag的名称里面, 那么就查找这个tag的所有别名 , 找到一个包含这个name的别名)
    #name 百度
    #query baidu
    #name.find(query) == -1
    #id - alias_list 
    #for i in alias_list : if i.find(query) >= 0  : return i
    pass

def tag_by_str(s):
    id_list = []
    name = map(utf8_ftoj,map(str.strip, s.split('/')))
    for i in name:
        id_list.append(tag_by_name(i))
    return id_list 




@mc_po_id_list_by_tag_id('{tag_id}')
def po_id_list_by_tag_id(tag_id, limit, offset=0):
    po_list = PoZsiteTag.where(zsite_id=tag_id).order_by('rank desc').col_list(limit, offset, col='po_id')
    return po_list


def po_by_tag(tag_id, user_id, limit=25, offset=0):
    id_list = po_id_list_by_tag_id(tag_id, limit, offset)
    return po_json(user_id, id_list, 36)

def tag_author_list(zsite_id):
    zsite_list = filter(lambda x:x, zsite_author_list(zsite_id))
    return zsite_json(zsite_id, zsite_list)

def zsite_tag_po_new_by_name(tag_name, po, rank):
    tag_name = tag_name.strip()
    tag = tag_by_str(tag_name)
    return zsite_tag_po_new(tag.id, po, rank)

def tag_rm_by_po(po):
    po_id = po.id
    user_id = po.user_id
    _tag_rm_by_user_id_list(user_id, tag_id_list_by_po_id(po_id))
    mc_flush_by_po_id(po_id)

def _tag_rm_by_user_id_list(user_id, id_list):
    for tag_id in id_list:
        PoZsiteTag.where(zsite_id=tag_id).delete()
        mc_flush_by_zsite_id(tag_id)

        user_rank = zsite_list_get(user_id, tag_id, CID_TAG)
        if not user_rank and user_rank.rank:
            user_rank.rank -= 1
            user_rank.save()



@mc_tag_id_list_by_po_id('{po_id}')
def tag_id_list_by_po_id(po_id):
    zsite_id_list = PoZsiteTag.where(po_id=po_id).col_list(col='zsite_id')
    return zsite_id_list

def mc_flush_by_po_id(po_id):
    mc_tag_id_list_by_po_id.delete(po_id)

def tag_list_by_po_id(po_id):
    zsite_id_list = tag_id_list_by_po_id(po_id)
    return Zsite.mc_get_list(zsite_id_list)

def po_tag_new_by_autocompelte(po, tag_list):
    tag_id_list = []
    for i in tag_id_list:
        if i.startswith('-'):
            for id in tag_by_str(i[1:]):
                tag_id_list.append(id)
        else:
            tag_id_list.append(i)
    return po_tag_id_list_new(po, unique(tag_id_list))

def po_tag_id_list_new(po, tag_id_list):
    po_id = po.id
    new_tag_id_list = set(map(int, tag_id_list))
    old_tag_id_list = set(tag_id_list_by_po_id(po_id))

    to_add = new_tag_id_list - old_tag_id_list
    to_rm = old_tag_id_list - new_tag_id_list

    user_id = po.user_id
    _tag_rm_by_user_id_list(user_id, to_rm)

    for tag_id in to_add:
        zsite_tag_po_new(tag_id, po)



#tag_rm_by_po_id(po.id)

#tag_id_list = tag_id_list.split(',')
#for tag in tag_id_list:
#    zsite_tag_po_new_by_name(tag, po, 100)

#tag_id_list = feed.tag_id_list.split(' '
#rec_read_new(po.id, tag_id_list)



if __name__ == '__main__':
    pass
    #print tag_list_by_po_id(69217)
    #print po_by_tag(1, 0)

    from model.po import Po,CID_NOTE
    for i in Po.where(cid=CID_NOTE).order_by("id desc")[:20]:
        po_tag_id_list_new(i, [137110])
