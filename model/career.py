#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from tag import tag_new, tag_get
from zkit.attrcache import attrcache
from zkit.mc_func import mc_func_get_dict
from spammer import anti_same_post
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME

CID_JOB = 1
CID_EDU = 2

CID_TUPLE = (
    (CID_JOB, 'job'),
#    (CID_EDU, 'edu'),
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
    return -cmp(a, b)


class Career(McModel):
    @attrcache
    def unit(self):
        return tag_get(self.unit_id)

    @attrcache
    def title(self):
        return tag_get(self.title_id)

    def __cmp__(self, other):
        end = end_cmp(self.end_time, other.end_time)
        if end == 0:
            return begin_cmp(self.begin_time, other.begin_time)
        return end

    @attrcache
    def value_list(self):
        return self.unit, self.title, self.txt, self.begin_time, self.end_time, self.id


def _career_new(user_id, unit_id, title_id, txt, begin, end, cid):

    o = Career(
        user_id=user_id,
        unit_id=unit_id,
        title_id=title_id,
        txt=txt,
        begin_time=begin,
        end_time=end,
        cid=cid,
    )
    o.save()

career_new = anti_same_post(_career_new)


def career_edit(id, user_id, unit_id, title_id, txt, begin, end, cid):
    o = Career.mc_get(id)
    if o and o.user_id == user_id and o.cid == cid:
        o.unit_id = unit_id
        o.title_id = title_id
        o.txt = txt
        o.begin_time = begin
        o.end_time = end
        o.save()

def career_rm(id, user_id):
    o = Career.mc_get(id)
    if o and o.user_id == user_id:
        o.delete()
        mc_flush(user_id, o.cid)

def career_set(id, user_id, unit, title, txt, begin, end, cid):
    if unit == '单位':
        unit = ''
    if title == '头衔':
        title = ''
    if txt.startswith('经历简述 '):
        txt = ''

    if not any((txt, title , unit)):
        career_rm(id, user_id)
        return
    user_id = int(user_id)
    unit_id = tag_new(unit)
    title_id = tag_new(title)
    begin = int(begin)
    end = int(end)
    if begin_end_cmp(begin, end) < 0:
        begin, end = end, begin
    if id:
        career_edit(id, user_id, unit_id, title_id, txt, begin, end, cid)
    else:
        career_new(user_id, unit_id, title_id, txt, begin, end, cid)

def career_list_set(id, user, unit, title, txt, begin, end, cid):
    user_id = user.id
    for id, unit, title, txt, begin, end in zip(id, unit, title, txt, begin, end):
        career_set(id, user_id, unit, title, txt, begin, end, cid)
    mc_flush(user_id, cid)
    from zsite_verify import zsite_verify_ajust
    zsite_verify_ajust(user)

@mc_career_id_list('{user_id}_{cid}')
def career_id_list(user_id, cid):
    li = Career.where(user_id=user_id, cid=cid)
    li = list(li)
    li.sort(reverse=True)
    return [i.id for i in li]

def career_job_id_list(user_id):
    return career_id_list(user_id, CID_JOB)

def career_list(user_id, cid):
    id_list = career_id_list(user_id, cid)
    li = Career.mc_get_list(id_list)
    return [i.value_list for i in li]

def career_list_all(user_id):
    id_list = career_id_list(user_id, CID_JOB)
    id_list.extend(career_id_list(user_id, CID_EDU))
    li = Career.mc_get_list(id_list)
    li.sort(reverse=True)
    return li


def career_current_str(user_id):
    t = career_current(user_id)
    t = ' , '.join(filter(bool, t))
    if t:
        t = ' ( %s )'%t
    return t

@mc_career_current('{user_id}')
def career_current(user_id):
    li = career_list_all(user_id)
    if li:
        o = li[0]
        return o.unit, o.title
    else:
        from user_school import user_school_tuple
        school = user_school_tuple(user_id)
        if school:
            school = school[0]
            school_id = school[1]
            if school_id:
                school_id = SCHOOL_UNIVERSITY[school_id]
            school_department = school[4]
            school_year = school[2]
            title2 = ''
            if school_department:
                title2 = SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[school_department]
            elif school_year:
                title2 = '%s 级'%school_year
            return  school_id or '', title2
    return '', ''


def career_dict(id_list):
    return mc_func_get_dict(
        mc_career_current,
        career_current,
        id_list,
    )


def career_bind(li, key='id'):
    d = set()
    for i in li:
        k = getattr(i, key)
        d.add(k)
    o_dict = career_dict(d)
    for i in li:
        i.career = o_dict.get(getattr(i, key))

def mc_flush(user_id, cid):
    from model.feed_po import mc_feed_user_dict
    mc_career_current.delete(user_id)
    mc_career_id_list.delete('%s_%s' % (user_id, cid))
    mc_feed_user_dict.delete(user_id)

if __name__ == '__main__':
    from yajl import dumps
