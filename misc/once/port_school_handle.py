#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
port_school.py
Author: WooParadog
Email:  Guohaochuan@gmail.com

Created on
2011-12-16
'''
import _env
from json import loads
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID, SCHOOL_DEGREE
from lcs import find_lcs_len

def handleSchool(school):
     school_id = [k for k,v in SCHOOL_UNIVERSITY.iteritems() if v==school[1]]
     if not school_id:
         match = [(i,find_lcs_len(v)) for i,v in SCHOOL_UNIVERSITY.iteritems()] 
         match = sorted(match,key=lambda x:x[0],reverse=True)[:5]
         raw_input( "\n".join([SCHOOL_UNIVERSITY[i[0]] for i in match]))

     dep_id = [ k for k,v in SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME.iteritems() if v==school[2]]
     if not dep_id:
         pass


def main():
    with open("port_school.txt") as f:
        for i in f:
            school=loads(i)

if __name__ == '__main__':
    pass
