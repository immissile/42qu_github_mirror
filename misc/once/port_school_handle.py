#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
port_school.py
Author: WooParadog Email:  Guohaochuan@gmail.com

Created on
2011-12-16
'''
import _env
from json import loads, dumps
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID, SCHOOL_DEGREE


MANUAL_LIST = []

def handleSchool(school):
    school_id = [k for k, v in SCHOOL_UNIVERSITY.iteritems() if v == school[1]]
    dep_id = [ k for k, v in SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME.iteritems() if v == school[2]]

    if school_id and dep_id:
        school_id = school_id[0]
        dep_id = dep_id[0]
        return (school[0], school_id, dep_id, school[3], school[4])

    MANUAL_LIST.append(school)

def main():
    w = open('out.txt', 'w')
    with open('port_school.txt') as f:
        for i in f:
            out = dumps(handleSchool(loads(i)))
            if out != 'null':
                w.write(out+'\n')

    open('to_be_verified', 'w').write(dumps(MANUAL_LIST))

if __name__ == '__main__':
    main()
