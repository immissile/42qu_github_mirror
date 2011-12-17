#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from json import loads, dumps
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID, SCHOOL_DEGREE
from lcs import LSS as find_lcs_len
from collections import defaultdict

log = open('further', 'w')

def getIndex(txt, max=10):
    gets = raw_input(txt)
    index = None
    if gets:
        try:
            index = int(gets)
            assert index < 10
        except:
            index = 100
    else:
        index = 100
    return index

def handle(school):

    name = school[1]
    name = name.replace('科技大学', '科大')
    name = name.replace('西安交通大学', '西安交大')
    name = name.replace('理工大学', '理工')
    name = name.replace('浙江工业大学', '浙江工大')
    name = name.replace('科学技术', '科技')
    name = name.replace('四川师范大学', '四川师大')
    name = name.replace('北航', '北京航空航天大学')
    name = name.replace('华中师范大学', '华中师大')
    name = name.replace('中国科学院', '中科院')
    name = name.replace('上海财经大学', '上海财经')
    name = name.replace('中国社会科学院', '中国社科院')
    name = name.replace('东北林业大学', '东北林大')
    name = name.replace('对外经济贸易大学', '对外经贸大学')
    name = name.replace('北大', '北京大学')
    name = name.replace('大连交通大学', '大连交大')
    name = name.replace('西南财经大学', '西南财经')
    name = name.replace('江西师范大学', '江西师大')
    name = name.replace('四川农业大学', '四川农大')
    name = name.replace('合肥工业大学', '合肥工大')
    name = name.replace('华东师范大学', '华东师大')
    name = name.replace('山东轻工业学院', '山东轻工')
    name = name.replace('上海师范大学', '上海师大')
    name = name.replace('中国地质大学', '中国地质大学（武汉）')
    name = name.replace('徐州师范大学', '徐州师大')
    name = name.replace('湖南师范大学', '湖南师大')
    name = name.replace('浙江传媒学院', '浙江传媒')

    match = []
    if name.replace(' ', '').isalpha():
        top = 2900110
    else:
        top = 34050

    school_id = [k for k, v in SCHOOL_UNIVERSITY.iteritems() if v == name]

    if not school_id:
        match = [(i, find_lcs_len(v.encode('utf-8'), name.encode('utf-8'))) for i, v in SCHOOL_UNIVERSITY.iteritems() if i <= top]
        match = sorted(match, key=lambda x:x[1], reverse=True)[:10]
        if match[0][1]>4:
            school_id = match[0][0]
        else:
            print '\n--------%s--------\n'% name
            get = getIndex('\n'.join(['选择:\t'+str(match.index(i))+' '+SCHOOL_UNIVERSITY[i[0]] for i in match]))
            if get < 10:
                school_id = match[get][0]
            else:
                log.write(dumps(school)+'\n')
                return
        print '\n\n++++++%s++++++++'%SCHOOL_UNIVERSITY[school_id]
    else:
        school_id = school_id[0]

    name = school[2]
    match = []
    depDict = defaultdict(str)
    dep_id = ' '
    if name.replace(' ', ''):
        if type(school_id) is int and school_id in SCHOOL_UNIVERSITY_DEPARTMENT_ID:
            for id in SCHOOL_UNIVERSITY_DEPARTMENT_ID[school_id]:
                depDict[id] = SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[id]
        else:
            depDict = SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME

        dep_id = [ k for k, v in depDict.iteritems() if v == name]

        if not dep_id:
            match = [(i, find_lcs_len(v.encode('utf-8'), name.encode('utf-8'))) for i, v in depDict.iteritems() ]
            match = sorted(match, key=lambda x:x[1], reverse=True)[:10]
            if match[0][1] > 4:
                dep_id = match[0][0]
            else:
                print '--------%s-------------'%school[2]
                get = getIndex('\n'.join(['选择:\t'+str(match.index(i))+' '+SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[i[0]] for i in match]))
                if get < 10:
                    dep_id = match[get][0]
                    print '\n\n++++++%s++++++++'%SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[dep_id], school_id
                else:
                    log.write(dumps(school)+'\n')
                    return
        else:
            dep_id = dep_id[0]

    return [school[0], school_id, dep_id]

def main():
    w = open('verified', 'w')
    with open('to_be_verified') as f:
        data = loads(f.read())
        count = 0
        for school in data:
            print '====%s===='%str(count)
            count += 1
            out = dumps(handle(school))
            if out != 'null':
                w.write(out+'\n')

if __name__ == '__main__':
    main()
