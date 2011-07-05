#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from tag import tag_new, tag_get
from zkit.attrcache import attrcache

CID_JOB = 1
CID_EDU = 2

CID_TUPLE = (
    (CID_JOB, 'job'),
    (CID_EDU, 'edu'),
)

CID_NAME = dict(CID_TUPLE)
CID_BY_STR = dict((v, k) for k, v in CID_TUPLE)

mc_career_id_list = McCacheA('CareerIdListCid.%s')
mc_career_current = McCacheM('CareerCurrent.%s')

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

    def value_list(self):
        return self.unit, self.title, self.txt, self.begin_time, self.end_time, self.id


def career_new(user_id, tag_id, title, txt, begin, end, cid):
    o = Career(
        user_id=user_id,
        tag_id=tag_id,
        title=title,
        txt=txt,
        begin_time=begin,
        end_time=end,
        cid=cid,
    )
    o.save()

def career_edit(id, user_id, tag_id, title, txt, begin, end, cid):
    o = Career.mc_get(id)
    if o and o.user_id == user_id and o.cid == cid:
        o.tag_id = tag_id
        o.title = title
        o.txt = txt
        o.begin_time = begin
        o.end_time = end_time
        o.save()

def career_set(id, user_id, unit, title, txt, begin, end, cid):
    user_id = int(user_id)
    tag_id = tag_new(unit)
    begin = int(begin)
    end = int(end)
    if begin_end_cmp(begin, end) < 0:
        begin, end = end, begin
    if id:
        career_edit(id, user_id, tag_id, title, txt, begin, end, cid)
    else:
        career_new(user_id, tag_id, title, txt, begin, end, cid)

def career_list_set(id, user_id, unit, title, txt, begin, end, cid):
    for id, unit, title, txt, begin, end in zip(id, unit, title, txt, begin, end)[:-1]:
        career_set(id, user_id, unit, title, txt, begin, end, cid)
    mc_career_current.delete(user_id)
    mc_career_id_list.delete('%s_%s' % (user_id, cid))

@mc_career_id_list('{user_id}_{cid}')
def career_id_list(user_id, cid):
    li = Career.where(user_id=user_id, cid=cid)
    li = list(li)
    li.sort(reverse=True)
    return [i.id for i in li]

def career_list(user_id, cid):
    id_list = career_id_list(user_id, cid)
    li = Career.mc_get_list(id_list)
    return [i.value_list for i in li]

@mc_career_current('{user_id}')
def career_current(user_id):
    li = Career.where(user_id=user_id)
    li = list(li)
    li.sort(reverse=True)
    if li:
        o = li[0]
        return o.unit, o.title
    return '', ''

from zkit.mc_func import mc_func_get_list, mc_func_get_dict

def career_bind(user_list):
    id_list = set([i.id for i in user_list])
    o_dict = mc_func_get_dict(
        mc_career_current,
        career_current,
        id_list,
    )
    for i in user_list:
        i.career = o_dict[i.id]
    return user_list

from zsite import Zsite
from cid import CID_USER

@attrcache
def user_career(self):
    if self.cid == CID_USER:
        return career_current(self.id)

Zsite.career = user_career

if __name__ == '__main__':
    from json import dumps
    dumps(career_list(2, 1))
