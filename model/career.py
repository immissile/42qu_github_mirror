#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA
from tag import tag_new

class Career(McModel):
    pass

def career_new(user_id, unit, title, txt, begin, end, cid):
    tag_id = tag_new(unit)
    c = Career(
        user_id=user_id,
        tag_id=tag_id,
        title=title,
        txt=txt,
        begin_time=begin,
        end_time=end,
        cid=cid,
    )
    c.save()

mc_career_id_list = McCacheA('CareerIdList.%s')

@mc_career_id_list('{user_id}_{cid}')
def career_id_list(user_id, cid):
    return Career.where(cid=cid).order_by('end_time desc').id_list()
