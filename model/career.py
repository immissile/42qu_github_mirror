#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA
from tag import tag_new, tag_get
from zkit.attrcache import attrcache

CID_JOB = 1
CID_EDU = 2

def end_cmp(a, b):
    if a == 0:
        if b == 0:
            return 0
        return 1
    if b == 0:
        return -1
    return cmp(a, b)

def begin_cmp(a, b):
    if a == 0:
        if b == 0:
            return 0
        return -1
    if b == 0:
        return 1
    return cmp(a, b)

def begin_end_cmp(a, b):
    if a == 0:
        if b == 0:
            return 0
        return 1
    if b == 0:
        return 1
    return cmp(a, b)


class Career(McModel):
    @attrcache
    def unit(self):
        return tag_get(self.tag_id)

    def __cmp__(self, other):
        end = end_cmp(self.end_time, other.end_time)
        if end == 0:
            return begin_cmp(self.begin_time, other.begin_time)
        return end


def career_new(user_id, unit, title, txt, begin, end, cid):
    tag_id = tag_new(unit)
    begin = int(begin)
    end = int(end)
    if begin_end_cmp(begin, end) < 0:
        begin, end = end, begin
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

def career_list_set(id, user_id, unit, title, txt, begin, end, cid):
    pass

mc_career_id_list = McCacheA('CareerIdListCid.%s')

@mc_career_id_list('{user_id}_{cid}')
def career_id_list(user_id, cid):
    return Career.where(user_id=user_id, cid=cid).order_by('end_time desc').col_list()

def career_list(user_id, cid):
    id_list = career_id_list(user_id, cid)
    li = Career.mc_get_list(id_list)
    return [(
        i.unit, i.title, i.txt, i.begin_time, i.end_time, i.id
    ) for i in li]

if __name__ == '__main__':
    from json import dumps
    dumps(career_list(2, 1))
