#!/usr/bin/env python
#coding:utf-8

def follow_new(from_id,to_id):
    from feed import mc_feed_id_by_for_zsite_follow
    mc_feed_id_by_for_zsite_follow.delete(from_id)

def follow_id_list_by_zsite_id(zsite_id):
    return []


