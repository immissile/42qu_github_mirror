#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, cursor_by_table, McCacheA, McLimitA
from zsite import Zsite
from cid import CID_FOLLOW
from gid import gid
from feed import feed_entry_rm, feed_entry_new, mc_feed_id_by_for_zsite_follow, mc_feed_entry_tuple

mc_follow_id_list_by_to_id = McLimitA('FollowIdListByToId.%s', 128)
mc_follow_id_list_by_from_id_cid = McCacheA('FollowIdListByFromIdCid.%s')
mc_follow_id_list_by_from_id = McCacheA('FollowIdListByFromId.%s')
mc_follow_get = McCache('FollowGet.%s')

class Follow(Model):
    pass

follow_cursor = cursor_by_table('follow')

@mc_follow_id_list_by_to_id('{to_id}')
def follow_id_list_by_to_id(to_id, limit, offset):
    follow_cursor.execute('select from_id from follow where to_id=%s order by id desc limit %s offset %s', (to_id, limit, offset))
    return [i for i, in follow_cursor]

@mc_follow_id_list_by_from_id('{from_id}')
def follow_id_list_by_from_id(from_id):
    follow_cursor.execute('select to_id from follow where from_id=%s', (from_id))
    return [i for i, in follow_cursor]

@mc_follow_id_list_by_from_id_cid('{from_id}_{cid}')
def follow_id_list_by_from_id_cid(from_id, cid):
    follow_cursor.execute('select to_id from follow where from_id=%s and cid=%s', (from_id, cid))
    return [i for i, in follow_cursor]

def follow_list_by_from_id_cid(from_id, cid):
    return Zsite.mc_get_list(
        follow_id_list_by_from_id_cid(from_id, cid)
    )

@mc_follow_get('{from_id}_{to_id}')
def follow_get(from_id, to_id):
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
    feed_entry_rm(id)
    to = Zsite.mc_get(to_id)
    mc_flush(from_id, to_id , to.cid)

def follow_new(from_id, to_id):
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
    feed_entry_new(id, from_id, CID_FOLLOW)
    from buzz import buzz_follow_new
    buzz_follow_new(from_id, to_id)
    mc_flush(from_id, to_id, cid)

def mc_flush(from_id, to_id, cid):
    mc_feed_id_by_for_zsite_follow.delete(from_id)
    mc_follow_get.delete( '%s_%s'%(from_id, to_id))
    mc_follow_id_list_by_from_id_cid.delete('%s_%s'%(from_id, cid))
    mc_follow_id_list_by_from_id.delete(from_id)


@mc_feed_entry_tuple('{id}')
def feed_tuple_follow(id):
    follow_cursor.execute(
        'select to_id from follow where id=%s',
        id
    )
    r = follow_cursor.fetchone()
    if r:
        zsite = Zsite.mc_get(r[0])
        return (zsite.name, zsite.link)
