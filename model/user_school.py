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


user_school_count = McNum(lambda school_id:UserSchool.where(school_id=school_id).count(), 'UserSchoolCount:%s')
user_school_year_count = McNum(lambda school_id, year:UserSchool.where(school_id=school_id, school_year=year).count(), 'UserSchoolYearCount:%s')

def mc_flush(user_id, school_id=0, year=0):
    mc_user_school_id_list.delete(user_id)
    mc_user_school_tuple.delete(user_id)
    from model.career import mc_career_current
    mc_career_current.delete(user_id)
    if school_id:
        user_school_count.delete(school_id)
        if year:
            user_school_year_count.delete('%s_%s'%(school_id, year))



@mc_user_school_id_list('{user_id}')
def user_school_id_list(user_id):
    return UserSchool.where(user_id=user_id).order_by('school_year desc, id desc').col_list()

def user_school_list(user_id):
    return UserSchool.mc_get_list(user_school_id_list(user_id))

def user_school_rm(id, user_id):
    us = UserSchool.mc_get(id=id)
    if us:
        us.delete()
        mc_flush(user_id, us.school_id, us.school_year)

@mc_user_school_tuple('{user_id}')
def user_school_tuple(user_id):
    return tuple(
        (i.id, i.school_id, i.school_year, i.school_degree, i.school_department, i.txt)
        for i in user_school_list(user_id)
    )


def user_school_json(user_id):
    return dumps(user_school_tuple(user_id))


def user_school_new(user_id, school_id, school_year, school_degree, school_department, txt='', id=None):
    if txt.startswith('经历简述 '):
        txt = ''
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
        mc_flush(user_id, school_id, school_year)
        return u




def user_school_search(school_id, school_year, school_department, school_degree):
    if not school_id:
        return []

    us = UserSchool.where(school_id=school_id)
    if user_school_count(school_id) > 32:
        if school_year:
            us = us.where(school_year=school_year)
            if user_school_year_count(school_id, year) > 32:
                if school_department:
                    us = us.where(school_department=school_department)
                if school_degree:
                    us = us.where(school_degree=school_degree)
                user_school_year_department_dergee_count
        else:
            count = user_school_count(school_id)     
    return result

if __name__ == '__main__':
    pass
    #print mc_flush(10000000)
    for i in SCHOOL_UNIVERSITY:
        if i:
            us = UserSchool.where(school_id=i)
            if us.count():
                print list(us)
                us.count()


