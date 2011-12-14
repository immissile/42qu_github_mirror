#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from zkit.job import JOBKIND2CN
from zsite_com import pid_by_com_id
from zkit.attrcache import attrcache
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID

class UserSchool(McModel):
    pass


def user_school_new(user_id, school_id, school_year, school_degree, school_department):
    school_id = int(school_id or 0)
    if school_id and school_id in SCHOOL_UNIVERSITY and user_id:
        school_year = int(school_year or 0)
        school_degree = int(school_degree or 0)
        school_department = int(school_department or 0)
        u = UserSchool(
            user_id=user_id,
            school_id=school_id,
            school_year=school_year,
            school_degree=school_degree,
            school_department=school_department
        )
        u.save()

        return u

if __name__ == '__main__':
    pass
