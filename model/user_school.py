#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from zkit.job import JOBKIND2CN
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_DEGREE
from json import dumps
from model.zsite import Zsite
from zkit.mc_func import mc_func_get_list
from model.zsite_rank import zsite_rank

mc_user_school_id_list = McCacheA('UserSchoolIdList:%s')
mc_user_school_tuple = McCacheM('UserSchoolTuple:%s')
mc_user_school_dict = McCacheM('UserSchoolDict<%s')

class UserSchool(McModel):
    pass


user_school_count = McNum(lambda school_id:UserSchool.raw_sql('select count(distinct(user_id)) from user_school where school_id=%s',school_id).fetchone()[0], 'UserSchoolCount:%s')


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
        mc_user_school_dict.delete(school_id)


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


def user_school_new(user, school_id, school_year, school_degree, school_department, txt='', id=None):
    user_id = user.id
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
        from zsite_verify import zsite_verify_ajust
        zsite_verify_ajust(user)
        return u


def user_school_search(school_id, school_year, school_degree, school_department):
    if not school_id:
        return []
    #result = user_school_dict(school_id)
    #zsite_id_list = []
    #for i in result:
    #    zsite_id_list.extend(i[1])
    #Zsite.mc_get_list(zsite_id_list)
    #result.sort(key=UserSchoolSorter(school_year,school_degree, school_department))
    #return result

    user_school = UserSchool.where(school_id=school_id)
    if school_year and int(school_year):
        user_school = user_school.where(school_year=school_year) 
    #if school_degree:
    #    user_school = user_school.where(school_degree=school_degree) 
    if school_department and int(school_department):
        user_school = user_school.where(school_department=school_department)
    id_list = user_school.col_list(col="user_id")
    rank_dict = zsite_rank.get_dict(id_list)
    items = sorted(rank_dict.iteritems(), key=lambda x:-x[1])
    return Zsite.mc_get_list(i[0] for i in items)


if __name__ == '__main__':
    for i in SCHOOL_UNIVERSITY:
        #r = user_school_search(i, 0 , 0, 0)
        t = user_school_search(i,0,0,0)
        if t:
            pass
            #print t
            
