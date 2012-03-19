#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA
from state import STATE_APPLY, STATE_ACTIVE
from mail import render_template, sendmail

mc_top_notice_id_by_user_id = McCache('TopNoticeIdByUserId.%s')


class TopNotice(McModel):
    pass


@mc_top_notice_id_by_user_id('{user_id}')
def top_notice_id_by_user_id(user_id):
    for i in TopNotice.where(user_id=user_id, state=1).order_by('id desc')[:1]:
        return i.id
    return 0

def top_notice_by_user_id(user_id):
    id = top_notice_id_by_user_id(user_id)
    if id:
        return TopNotice.mc_get(id)

def top_notice_new(user_id, cid, rid):
    o = TopNotice(user_id=user_id, cid=cid, rid=rid, state=1)
    o.save()
    mc_top_notice_id_by_user_id.set(user_id, o.id)
    return o

def top_notice_rm(id, user_id):
    o = TopNotice.mc_get(id)
    if o and o.user_id == user_id:
        o.state = 0
        o.save()
        mc_top_notice_id_by_user_id.delete(user_id)


if __name__ == '__main__':
    pass
