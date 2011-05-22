#!/usr/bin/env python
#coding:utf-8
from _db import Model, McModel, McCache, cursor_by_table
from zsite import Zsite
from cid import CID_FOLLOW
from feed import feed_entry_new
#TODO  follow 进入消息流

mc_follow_get = McCache("FollowGet:%s")

follow_cursor = cursor_by_table("follow")

@mc_follow_get("{from_id}_{to_id}")
def follow_get(from_id, to_id):
    follow_cursor.execute(
        "select 1 from follow where from_id=%s and to_id=%s",
        (from_id, to_id)
    )
    result = follow_cursor.fetchone()
    if result:
        return result[0]
    return False

def follow_rm(from_id, to_id):
    follow_cursor.execute(
        "delete from follow where from_id=%s and to_id=%s",
        (from_id, to_id)
    )
    mc_follow_get.delete("%s_%s"%(from_id, to_id))

def follow_new(from_id, to_id):
    to = Zsite.mc_get(to_id)
    if not to:
        return
    if follow_get(from_id, to_id):
        return

    id = gid(),
    follow_cursor.execute(
        "insert into follow (id, from_id, to_id, cid) values (%s,%s,%s)",
        (id, from_id, to_id, to.cid)
    )
    follow_cursor.connection.commit()
    #feed_entry_new(id, from_id, CID_FOLLOW)
    from feed import mc_feed_id_by_for_zsite_follow
    mc_feed_id_by_for_zsite_follow.delete(from_id)
    mc_follow_get.set("%s_%s"%(from_id, to_id), 1)

def follow_id_list_by_zsite_id(zsite_id):
    return []

