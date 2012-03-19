#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from json import loads, dumps
from zkit.school_university import SCHOOL_UNIVERSITY, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME, SCHOOL_UNIVERSITY_DEPARTMENT_ID
from lcs import LSS as find_lcs_len
from collections import defaultdict
from zkit.fanjian import ftoj
from random import shuffle

def replace_name(name):
    name = ftoj(name.decode('utf-8'))
    if type(name) is unicode:
        name = name.encode('utf-8')
    name = name.replace('大学', '大').replace('科学技术', '科').replace('中国', '中').replace('师范', '师').replace('科技', '科').replace('交通', '交').replace('财经', '财').replace('工业', '工').replace('北京', '北').replace('科学', '科').replace('农业', '农').decode('utf-8')
    if name.endswith(u"大") and len(name) > 2:
        name = name[:-1]
    return name

with open('to_be_verified', 'r') as to_be_verifyed:
    data = loads(to_be_verifyed.read())
    #shuffle(data)

_SCHOOL_UNIVERSITY = dict((replace_name(v), k) for k, v in SCHOOL_UNIVERSITY.iteritems())


f = open('out2.txt', 'w')
err = open('logging2','w')
fcount = 0
for pos, i in enumerate(data):

    _name = i[1]
    name = replace_name(_name)
    print name
    if not name: continue
    c = []
    maxlen = 0

    for j, id in _SCHOOL_UNIVERSITY.iteritems():
        if len(set(name)&set(j)) >= 2:
            llen = find_lcs_len(name, j)
            if llen > maxlen:
                c = [j]
                maxlen = llen
            elif llen == maxlen:
                c.append(j)
    ok = False
    if c:
        c.sort(key=len)
        #    print " ".join(c)
        if (maxlen / float(len(name)) ) > 0.6 and maxlen/float(len(c[0])) > 0.6:
            ok = True

    if ok:
        name = i[2].encode('utf-8')
        p = []
        maxlen = 0

        depDict = defaultdict(str)

        pok = False
        if _SCHOOL_UNIVERSITY[c[0]] in SCHOOL_UNIVERSITY_DEPARTMENT_ID:
            for id in SCHOOL_UNIVERSITY_DEPARTMENT_ID[_SCHOOL_UNIVERSITY[c[0]]]:
                depDict[SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[id]] = id

            for j, id in depDict.iteritems():
                if len(set(name)&set(j)) >= 2:
                    llen = find_lcs_len(name, j.encode('utf-8'))
                    if llen > maxlen:
                        p = [j]
                        maxlen = llen
                    elif llen == maxlen:
                        p.append(j)
            if p:
                p.sort(key=len)
                if (maxlen / float(len(name)) ) > 0.4 and maxlen/float(len(p[0])) > 0.4:
                    pok = True

        if pok:
            print name, SCHOOL_UNIVERSITY_DEPARTMENT_ID2NAME[depDict[p[0]]]
            f.write("\n"+dumps([i[0],_SCHOOL_UNIVERSITY[c[0]],depDict[p[0]],i[3],i[4]]))
            f.flush()
        else:
            f.write("\n"+dumps([i[0],_SCHOOL_UNIVERSITY[c[0]],' ',i[3],i[4]]))
            f.flush()
            pass
        pass

    else:
        fcount += 1
        err.write("\n" + dumps(i))
        err.flush()

    #    print  _name
    #    print  SCHOOL_UNIVERSITY[_SCHOOL_UNIVERSITY[c[0]]]
    #    print ".........."
    #if pos%30 == 1:
    #    raw_input('----------')
    print pos, fcount

