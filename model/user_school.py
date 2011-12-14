#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA
from zkit.job import JOBKIND2CN
from zsite_com import pid_by_com_id
from zkit.attrcache import attrcache
from zkit.school_university import SCHOOL_UNIVERSITY

class UserSchool(McModel):
    pass

def user_school_new(user_id, school_id, school_year, school_degree, school_department):
    school_id = int(school_id)
    if school_id and school_id in SCHOOL_UNIVERSITY and user_id:
        school_year = int(school_year)
        school_degree = int(school_degree)
        school_department = int(school_department)
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
