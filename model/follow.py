#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, cursor_by_table, McCacheA, McLimitA, McNum, McCacheM
from zsite import Zsite
from gid import gid
from days import ONE_DAY
from zsite_url import name_dict_url_dict_by_zsite_id_list
from model.cid import CID_USER
from zkit.mc_func import mc_func_get_dict_with_key_pattern

follow_count_by_to_id = McNum(lambda to_id: Follow.where(to_id=to_id).count(), 'FollowCountByToId.%s')
follow_count_by_from_id = McNum(lambda from_id: Follow.where(from_id=from_id).count(), 'FollowCountByFromId.%s')
mc_follow_id_list_by_to_id = McLimitA('FollowIdListByToId.%s', 128)
mc_follow_id_list_by_from_id_cid = McCacheA('FollowIdListByFromIdCid.%s')
mc_follow_id_list_by_from_id = McCacheA('FollowIdListByFromId.%s')
mc_follow_get = McCache('FollowGet<%s')
mc_following_id_rank_tuple = McCacheM('FollowingIdRankTuple.%s')


class Follow(Model):
    pass

follow_cursor = cursor_by_table('follow')

@mc_follow_id_list_by_to_id('{to_id}')
def follow_id_list_by_to_id(to_id, limit, offset):
    follow_cursor.execute('select from_id from follow where to_id=%s order by id desc limit %s offset %s', (to_id, limit, offset))
    return [i for i, in follow_cursor]

@mc_follow_id_list_by_from_id('{from_id}')
def follow_id_list_by_from_id(from_id):
    follow_cursor.execute('select to_id from follow where from_id=%s order by id desc', (from_id))
    return [i for i, in follow_cursor]

@mc_following_id_rank_tuple('{from_id}', ONE_DAY)
def following_id_rank_tuple(from_id):
    from model.zsite_rank import zsite_rank
    id_list = follow_id_list_by_from_id(from_id)
    rank_list = zsite_rank.get_list(id_list)
    t = zip(id_list, rank_list)[:512]
    return tuple(t)

def follow_list_show_by_from_id(from_id, limit):
    from operator import itemgetter
    from zkit.algorithm.wrandom import wsample_k2
    following_tuple = following_id_rank_tuple(from_id)
    f = wsample_k2(following_tuple, limit, key=itemgetter(1))
    id_list = [i[0] for i in f()]
    return Zsite.mc_get_list(id_list)

@mc_follow_id_list_by_from_id_cid('{from_id}_{cid}')
def follow_id_list_by_from_id_cid(from_id, cid):
    follow_cursor.execute('select to_id from follow where from_id=%s and cid=%s order by id desc', (from_id, cid))
    return [i for i, in follow_cursor]

def follow_list_by_from_id_cid(from_id, cid):
    id_list = follow_id_list_by_from_id_cid(from_id, cid)
    return Zsite.mc_get_list(id_list)


def follow_name_dict_url_dict_by_from_id_cid(from_id, cid):
    flist = follow_id_list_by_from_id_cid(from_id, cid)
    return name_dict_url_dict_by_zsite_id_list(flist)

def follow_reply_name_dict_url_dict_by_from_id_cid(from_id, po_id):
    flist = set(follow_id_list_by_from_id_cid(from_id, CID_USER))
    from model.po import Po
    po = Po.mc_get(po_id)
    flist.update(po.reply_zsite_id_list())
    return name_dict_url_dict_by_zsite_id_list(flist)


def follow_get(from_id, to_id):
    if from_id and to_id:
        if from_id == to_id:
            return True
        else:
            return _follow_get(from_id, to_id)
    return False

@mc_follow_get('{from_id}_{to_id}')
def _follow_get(from_id, to_id):
    follow_cursor.execute(
        'select id from follow where from_id=%s and to_id=%s',
        (from_id, to_id)
    )
    result = follow_cursor.fetchone()
    if result:
        return result[0]
    return 0




def follow_rm(from_id, to_id):
    id = follow_get(from_id, to_id)
    if not id:
        return
    follow_cursor.execute(
        'delete from follow where id=%s', id
    )
    to = Zsite.mc_get(to_id)
    mc_flush(from_id, to_id, to.cid)
    return True

def follow_new(from_id, to_id):
    if not _follow_new(from_id, to_id):
        return
    return True

def _follow_new(from_id, to_id):
    if follow_get(from_id, to_id):
        return True
    if from_id == to_id:
        return
    to = Zsite.mc_get(to_id)
    if not to:
        return
    if follow_get(from_id, to_id):
        return
    cid = to.cid
    id = gid()
    follow_cursor.execute(
        'insert into follow (id, from_id, to_id, cid) values (%s,%s,%s,%s)',
        (id, from_id, to_id, cid)
    )
    follow_cursor.connection.commit()
    mc_flush(from_id, to_id, cid)
    if cid == CID_USER:
        from model.autocomplete_user import autocomplete_user
        autocomplete_user.rank_update(
            to_id, follow_count_by_to_id(to_id)
        )
    return True

def mc_flush(from_id, to_id, cid):
    mc_follow_get.delete('%s_%s'%(from_id, to_id))
    mc_follow_id_list_by_from_id_cid.delete('%s_%s'%(from_id, cid))
    mc_follow_id_list_by_from_id.delete(from_id)
    mc_following_id_rank_tuple.delete(from_id)
    mc_follow_id_list_by_to_id.delete(to_id)
    follow_count_by_to_id.delete(to_id)
    follow_count_by_from_id.delete(from_id)

def follow_get_list(from_id, to_id_list):
    if not from_id:
        return [0]*len(to_id_list)

    _id_list = [
        (from_id, i) for i in to_id_list if i != from_id and i
    ]

    _follow_result = mc_func_get_dict_with_key_pattern(
        mc_follow_get,
        _follow_get,
        _id_list,
        '%s_%s'
    )
    _dict = dict(
        (i[1], _follow_result[i]) for i in _id_list
    )
    result = []
    for i in to_id_list:
        if not i:
            result.append(False)
        elif from_id == i:
            result.append(True)
        else:
            result.append(_dict[i])
    return result


if __name__ == '__main__':
    #print follow_get(10001955, 10000217)
    #print mc_follow_id_list_by_to_id
    #print following_id_rank_tuple(10000000)
    #print follow_list_show_by_from_id(10000000, 1)
    from yajl import dumps
    print dumps(follow_get_list(10001955, [10000217, 10001955]))
