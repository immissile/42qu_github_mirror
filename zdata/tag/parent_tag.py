#coding:utf-8
import _env
from name2id import NAME2ID
from zkit.txt_cleanup import sp_txt
from collections import defaultdict
from zkit.pprint import pprint

sp2id = defaultdict(list)

for k, v in NAME2ID.iteritems():
    for i in sp_txt(k):
        sp2id[i].append(k)

word_parent = defaultdict(set)

for k, v in NAME2ID.iteritems():
    for i in sp_txt(k):
        for j in sp2id[i]:
            if j != k and k in j:
                #print k, j
                word_parent[NAME2ID[j]].add(NAME2ID[k])

id2name = dict((k, v) for v, k in NAME2ID.iteritems())

#for id, pid_list in word_parent.iteritems():
#    print id2name[id]
#    for i in pid_list:
#        print id2name[i],
#    print "\n" 

word_parent = dict((k, tuple(v)) for k, v in word_parent.iteritems())

print 'PTAG = ',
pprint(word_parent)


