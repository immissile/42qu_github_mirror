#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys;
reload(sys);
sys.setdefaultencoding('utf-8')


from yajl import loads, dumps

def main():
    with open('relations/topic_dict')as f:
        topic_dict = dict([(v,k) for k,v in loads(f.read()).items()])
    with open('relations/topic_member') as f:
        topic_member = loads(f.read())
    topic_member = sorted(topic_member.iteritems(),key=lambda x:len(x[1]),reverse = True)
    for k,v in topic_member:
        print len(v) ,' - ',topic_dict[int(k)]
    pass


if __name__ == '__main__':
    main()
