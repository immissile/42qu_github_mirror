#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from zkit.job import JOBKIND2CN
from zsite_com import pid_by_com_id
from zkit.attrcache import attrcache
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID, SCHOOL_DEGREE
from json import dumps

mc_user_school_id_list = McCacheA('UserSchoolIdList:%s')
mc_user_school_tuple = McCacheM('UserSchoolTuple:%s')

class UserSchool(McModel):
    pass

def mc_flush(user_id):
    mc_user_school_id_list.delete(user_id)
    mc_user_school_tuple.delete(user_id)

@mc_user_school_id_list('{user_id}')
def user_school_id_list(user_id):
    return UserSchool.where(user_id=user_id).order_by('school_year desc, id desc').col_list()

def user_school_list(user_id):
    return UserSchool.mc_get_list(user_school_id_list(user_id))

def user_school_rm(id, user_id):
    UserSchool.where(id=id, user_id=user_id).delete()
    mc_flush(user_id)

@mc_user_school_tuple('{user_id}')
def user_school_tuple(user_id):
    return tuple(
        (i.id, i.school_id, i.school_year, i.school_degree, i.school_department, i.txt)
        for i in user_school_list(user_id)
    )


def user_school_json(user_id):
    return dumps(user_school_tuple(user_id))


def user_school_new(user_id, school_id, school_year, school_degree, school_department, txt='', id=None):
    school_id = int(school_id or 0)
    if school_id and school_id in SCHOOL_UNIVERSITY and user_id:
        school_year = int(school_year or 0)
        school_degree = int(school_degree or 0)
        school_department = int(school_department or 0)

        if school_year and school_year < 1000:
            return
        if school_degree and school_degree not in SCHOOL_DEGREE:
            return
        if school_department and school_department not in SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME:
            return

        if id:
            u = UserSchool.mc_get(id)
        else:
            u = UserSchool()

        u.user_id = user_id
        u.school_id = school_id
        u.school_year = school_year
        u.school_degree = school_degree
        u.school_department = school_department
        u.txt = txt
        u.save()
        mc_flush(user_id)
        return u

if __name__ == '__main__':
    pass
    print user_school_json(10000000)
