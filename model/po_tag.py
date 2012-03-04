#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis
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
#from zkit.pprint import pprint
from zkit.fanjian import utf8_ftoj
from fav import fav_user_count_by_po_id
from zrank.sorts import hot
from operator import itemgetter
from rec_read import rec_read_new, rec_read_user_topic_score_incr, REDIS_REC_PO_SCORE, REDIS_REC_TAG_NEW, REDIS_REC_TAG_OLD 

#REDIS_REC_CID_BUZZ =  6

REDIS_REC_CID_TUPLE = (
    (1, '快讯'),
    (2, '文章'),
    (3, '讨论'),
#    (4, '人物 / 对话'),
#    (5, '资料 / 知识'),
#    (REDIS_REC_CID_BUZZ, '碎语 / 片段'),
)
REDIS_REC_CID_DICT = dict(REDIS_REC_CID_TUPLE)

class TagAlias(McModel):
    #id, tag_id, name
    #tag_id->cluster index
    #name -> index
    pass

mc_po_id_list_by_tag_id = McLimitA('PoIdListByTagId.%s', 512)
mc_tag_id_list_by_po_id = McCacheA('TagIdListByPoId.%s')
zsite_tag_po_count = McNum(
    lambda tag_id: PoZsiteTag.where(zsite_id=tag_id).count(),
    'ZsiteTagPoCount:%s'
)

REDIS_ALIAS = 'TagAlias:%s'
REDIS_ALIAS_NAME2ID = 'AliasName2Id'

REDIS_TAG_CID = 'TagCid:%s:%s'
REDIS_TAG_CID_COUNT = 'TagCid=%s'
REDIS_PO_ID2TAG_CID = 'PoId2TagCid'

class PoZsiteTag(Model):
    pass

def tag_cid_by_po_id(po_id):
    if not po_id:
        return 0
    return redis.hget(REDIS_PO_ID2TAG_CID, po_id) or 0

def po_score_incr(po, user_id, score=1):
    po_id = po.id
    cid = tag_cid_by_po_id(po_id)
    tag_id_list = tag_id_list_by_po_id(po_id=po_id)
    if tag_id_list:
        redis.hincrby(REDIS_REC_PO_SCORE, po_id, score) 
        for tag_id in tag_id_list:
            rec_read_user_topic_score_incr(user_id, tag_id, score)
            if cid:
                key = REDIS_TAG_CID%(tag_id, cid)
                redis.zadd(key, po_id, po_score(po))

def po_score(po):
    po_id = po.id
    score = int(redis.hget(REDIS_REC_PO_SCORE, po_id)) 
    return hot(score, 0, po.create_time)
    

#def section_list_by_tag_id_cid(tag_id, cid):
#    key = REDIS_TAG_CID%(tag_id, cid)
#    id_list = redis.zrevrange(key, 0, -1, True)
#    return id_list

#def section_rank_refresh(po):


def _zsite_tag_po_new(zsite_id, po, cid, rank=1):
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

    rec_read_new(po_id, zsite_id)
    if cid in REDIS_REC_CID_DICT:

        p = redis.pipeline()

        #将分数放到相应的ranged set里面
        key = REDIS_TAG_CID%(zsite_id, cid)
        p.zadd(key, po_id, hot(1, 0, po.create_time))

        key = REDIS_TAG_CID_COUNT%zsite_id
        p.hincrby(key, cid, 1)

        p.execute()

    return tag_po




def mc_flush(zsite_id, po_id):
    mc_flush_by_zsite_id(zsite_id)
    mc_flush_by_po_id(po_id)

def mc_flush_by_zsite_id(zsite_id):
    zsite_tag_po_count.delete(zsite_id)
    mc_po_id_list_by_tag_id.delete(zsite_id)

def zsite_author_list(zsite_id):
    return Zsite.mc_get_list(zsite_id_list(zsite_id, CID_TAG))



def tag_mv(id, new_name):
    #TODO:修改一个标签.
    '''
    修改数据库中的,
    修改redis中的, NAME2ID, 和别名用到的几个.
    '''
    pass

def tag_rm(id):
    #TODO:删除一个标签.
    '''
    数据库, redis: NAME2ID, zset, 以及别名用到的几个.
    '''
    pass

def tag_new(name):
    found = Zsite.get(name=name, cid=CID_TAG)
    if not found:
        found = zsite_new(name, CID_TAG)

    id = found.id

    #1. 更新autocompelete
    from model.autocomplete import  autocomplete_tag
    autocomplete_tag.append(name, id)
    #2. 更新别名库

    for i in map(utf8_ftoj, map(str.strip, name.split('/'))):
        _tag_alias_new(id, i)

    return id

def _tag_alias_new(id, name):
    low = name.lower()
    redis.sadd(REDIS_ALIAS%id, low)


def tag_by_name(name):
    low = name.lower()
    id = redis.hget(REDIS_ALIAS_NAME2ID, low)
    if not id:
        id = tag_new(name)
    return id

def tag_alias_new(id, name, rank=1):
    from model.autocomplete import  autocomplete_tag
    #添加别名
    low = name.lower()
    oid = redis.hget(REDIS_ALIAS_NAME2ID, low)
    if oid:
        return

    tag_alias = TagAlias.get_or_create(name=name)
#    if not id:
#        print id, name
#        raw_input()
    tag_alias.tag_id = id
    tag_alias.save()

    _tag_alias_new(id, name)
    redis.hset(REDIS_ALIAS_NAME2ID, name, id)
    autocomplete_tag.append_alias(name, id)

def tag_alias_rm(alias_id):
    from model.autocomplete import  autocomplete_tag
    #Remove redis
    low = name.lower()
    tag_alias = TagAlias.get(alias_id)
    if tag_alias:
        id = tag_alias.tag_id
        name = tag_alias.name
        redis.srem(REDIS_ALIAS%id, low)
        redis.hdel(REDIS_ALIAS_NAME2ID, name)
        tag_alias.delete()
        autocomplete_tag.pop_alias(name, id)

def tag_alias_by_id(id):
    #TODO:放在mysql
    tag_alias_list = TagAlias.where(tag_id=id).col_list(col='name')
    return tag_alias_list

def tag_alias_by_id_query(id, query):
    #根据 id 和 name 返回别名 (自动补全提示的时候, 如果输入的字符串 lower以后不在tag的名称里面, 那么就查找这个tag的所有别名 , 找到一个包含这个name的别名)
    #name 百度
    #query baidu
    #name.find(query) == -1
    #id - alias_list 
    #for i in alias_list : if i.find(query) >= 0  : return i
    alias_list = redis.smembers(REDIS_ALIAS%id)
    for i in alias_list:
        if query in i:
            return i

def tag_by_str(s):
    id_list = []
    name = map(utf8_ftoj, map(str.strip, s.split('/')))
    for i in name:
        id_list.append(tag_by_name(i))
    return id_list

@mc_po_id_list_by_tag_id('{tag_id}')
def po_id_list_by_tag_id(tag_id, limit, offset=0):
    po_list = PoZsiteTag.where(zsite_id=tag_id).order_by('rank desc').col_list(limit, offset, col='po_id')
    return po_list

def po_tag(tag_id, user_id, limit=25, offset=0):
    id_list = po_id_list_by_tag_id(tag_id, limit, offset)
    return po_json(user_id, id_list, 36)



def tag_author_list(zsite_id):
    zsite_list = filter(lambda x:x, zsite_author_list(zsite_id))
    return zsite_json(zsite_id, zsite_list)

def po_tag_rm_by_po(po):
    po_id = po.id
    user_id = po.user_id
    _tag_rm_by_user_id_list(po, user_id, tag_id_list_by_po_id(po_id))
    mc_flush_by_po_id(po_id)

def _tag_rm_by_user_id_list(po, user_id, id_list):

    for tag_id in id_list:

        PoZsiteTag.where(zsite_id=tag_id).delete()
        mc_flush_by_zsite_id(tag_id)

        user_rank = zsite_list_get(user_id, tag_id, CID_TAG)
        if not user_rank and user_rank.rank:
            user_rank.rank -= 1
            user_rank.save()

    po_id = po.id
    cid = tag_cid_by_po_id(po_id)

    if cid:
        p = redis.pipeline()

        for tag_id in id_list:
            #将分数放到相应的ranged set里面
            key = REDIS_TAG_CID%(tag_id, cid)
            p.zrem(key, po_id)

            key = REDIS_TAG_CID_COUNT%tag_id
            p.hincrby(key, cid, -1)

            for i in (REDIS_REC_TAG_NEW, REDIS_REC_TAG_OLD):
                key = i%tag_id
                p.zrem(key, po_id)
        p.execute()

def _po_tag_id_cid_new(po, tag_id_list, cid):
    po_id = po.id
    old_cid = tag_cid_by_po_id(po_id)

    set_cid = False
    if old_cid:
        if old_cid != cid:
            score = po_score(po)

            p = redis.pipeline()
            for tag_id in tag_id_list:
                old_key = REDIS_TAG_CID%(tag_id, old_cid)
                p.zrem(old_key, po_id)
                if cid in REDIS_REC_CID_DICT:
                    new_key = REDIS_TAG_CID%(tag_id, cid)
                    p.zadd(new_key, po_id, score)
            p.execute()


@mc_tag_id_list_by_po_id('{po_id}')
def tag_id_list_by_po_id(po_id):
    zsite_id_list = PoZsiteTag.where(po_id=po_id).col_list(col='zsite_id')
    return zsite_id_list

def mc_flush_by_po_id(po_id):
    mc_tag_id_list_by_po_id.delete(po_id)

def tag_list_by_po_id(po_id):
    zsite_id_list = tag_id_list_by_po_id(po_id)
    return Zsite.mc_get_list(zsite_id_list)

def tag_id_list_by_str_list(tag_list):
    tag_id_list = []
    for i in tag_list:
        i_ = i.startswith('-')
        if i_:
            i_ = i[1:]
        if i_ or not i.isdigit():
            for id in tag_by_str(i):
                tag_id_list.append(id)
        else:
            tag_id_list.append(i)
    return unique(map(int,tag_id_list))


def po_tag_new_by_autocompelte(po, tag_list, cid=0):
    return po_tag_id_list_new(po, tag_id_list_by_str_list(tag_list), cid)

#def po_tag_id_new(po, tag_id, cid):
#    if cid:
#        cid = int(cid)
#        if cid not in REDIS_REC_CID_DICT:
#            cid = 0
#    if not cid:
#        cid = REDIS_REC_CID_BUZZ 
#
#    po_id = po.id
#    
#    old_tag_id_list = set(tag_id_list_by_po_id(po_id))
#    old_tag_id_list.add(tag_id)
#    
#    po_tag_id_cid_new(po, old_tag_id_list, cid)
#    po_tag_id_list_new(po, tag_id_list, cid=cid)


    
def po_tag_id_list_new(po, tag_id_list, cid=0):
    cid = int(cid)

    po_id = po.id
    new_tag_id_list = set(map(int, tag_id_list))
    old_tag_id_list = set(tag_id_list_by_po_id(po_id))

    to_add = new_tag_id_list - old_tag_id_list
    to_rm = old_tag_id_list - new_tag_id_list

     
    _po_tag_id_cid_new(po, old_tag_id_list - to_rm, cid)

    user_id = po.user_id
    _tag_rm_by_user_id_list(po, user_id, to_rm)

    for tag_id in to_add:
        _zsite_tag_po_new(tag_id, po, cid)

    if cid:
        #将po放在相应的po_id=>cid中
        redis.hset(REDIS_PO_ID2TAG_CID, po_id, cid)


def tag_cid_count(tag_id, cid=None):
    key = REDIS_TAG_CID_COUNT%tag_id
    if cid is None:
        count_dict = redis.hgetall(key)
        r = []
        for k, v in count_dict.iteritems():
            r.append((int(k), int(v)))
        r.sort(key=itemgetter(0))
        return r
    else:
        return redis.hget(key, cid)

def po_id_list_by_tag_id_cid(tag_id, cid, limit, offset):
    id_list = redis.zrange( REDIS_TAG_CID%(tag_id, cid), offset, limit+offset-1 )
    return id_list

def po_tag_by_cid(cid, tag_id, user_id, limit=25, offset=0):
    id_list = po_id_list_by_tag_id_cid(tag_id, cid, limit, offset)
    return po_json(user_id, id_list, 45)


if __name__ == '__main__':
    pass

    #Print tag_cid_count(10225558)

    #For a,b in REDIS_REC_CID_TUPLE:
    #    print tag_cid_count(10225558,a)

    #tag_id = 10233328
    #user_id = 10014918
    #print po_tag_by_cid(4, tag_id, user_id,)
#    print po_json(po_id_list_tag_id_cid(10233328, 4, 5, 0))
    #print po_json(po_id_list_tag_id_cid(10233328, 4, 5, 0))


    #for tag_cid, count in tag_cid_count(10233568):
        #print REDIS_REC_CID_DICT [tag_cid]

    #from model.po import Po
    #po = Po.where()[1]
    #print po
    #po_tag_new_by_autocompelte(po, ['-张沈鹏'], 1)
    #print tag_cid_count(10232177)

    #print po_tag_id_cid(10232177, 1, 1, 0)

#    print tag_id_list_by_str_list(['张沈鹏'])


