#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from json import loads, dumps
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID
from lcs import LSS as find_lcs_len
from collections import defaultdict

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
    match = []

    if name.replace(' ', '').isalpha():
        top = 2900110
    else:
        top = 34050

    school_id = [k for k, v in SCHOOL_UNIVERSITY.iteritems() if v == name]

    if not school_id:
        match = [(i, find_lcs_len(v.encode('utf-8'), name.encode('utf-8'))) for i, v in SCHOOL_UNIVERSITY.iteritems() if i <= top]
        match = sorted(match, key=lambda x:x[1], reverse=True)[:10]

        print '\n--------%s--------\n'% name
        get = getIndex('\n'.join(['选择:\t'+str(match.index(i))+' '+SCHOOL_UNIVERSITY[i[0]] for i in match]))
        if get < 10:
            school_id = match[get][0]
        else:
            school_id = 0
        if school_id:
            print '\n\n++++++%s++++++++'%SCHOOL_UNIVERSITY[school_id]

    else:
        school_id = school_id[0]

    name = school[2]
    match = []
    depDict = defaultdict(str)
    dep_id = 0
    if name.replace(' ', ''):
        if school_id and type(school_id) is int and school_id in SCHOOL_UNIVERSITY_DEPARTMENT_ID:
            for id in SCHOOL_UNIVERSITY_DEPARTMENT_ID[school_id]:
                depDict[id] = SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[id]
        else:
            depDict = SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME

        dep_id = []
        for k,v in depDict.iteritems():
            mlen = find_lcs_len(name.encode('utf-8'),v.encode('utf-8'))
            if mlen > 3:
                dep_id.append((k,mlen))

        dep_id.sort(key=lambda x:x[1])

        if not dep_id:
            dep_id = 0
        else:
            dep_id = dep_id[0][0]
            print name,SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[dep_id]

    return [school[0], school_id, dep_id]

def main():
    w = open('verified', 'aw')
    handled = open('logging').read().split()
    logging = open('logging','w')
    
    for i in handled:
        logging.write("\n"+i)

    with open('logging2') as f:
        count = 0
        for school in f:
            if str(count) not in handled and len(school)>1:
                print '====%s===='%str(count)

                data = loads(school)
                out = dumps(handle(data))
                if out != 'null':
                    w.write('\n'+out)
                logging.write("\n"+str(count))
            count += 1


def ba():
    a = open("verified")
    b = open("logging2")
    new = open("newestEx","w")
    extraInfo= []
    out = []
    for line in b:
        extraInfo.append(loads(line))

    for pos,data in enumerate(a):
        olddata = loads(data)
        olddata.extend([extraInfo[pos][3],extraInfo[pos][4]])
        new.write(dumps(olddata)+"\n")


if __name__ == '__main__':
    ba()
