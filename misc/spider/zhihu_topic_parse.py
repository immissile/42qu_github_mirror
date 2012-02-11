#coding:utf-8

from zhihu_topic_data import ZHIHU_TOPIC
from collections import defaultdict

NAME_COUNT = defaultdict(int)

def name_rank():
    for id, _name , url , img, rank in ZHIHU_TOPIC:
        name = _name
        id = int(id)
        if "知乎" in name and "知乎"!=name: 
            continue
        name = name.replace('|', '-')
        name = [
            i.replace('）', '')
            for i in
            name.split('（')
        ]
        yield _name , name, rank

for name, rank in name_rank():
    for i in name:
        NAME_COUNT[i] += 1

TAG_TAG = set()
for k, v in NAME_COUNT.iteritems():
    if v > 3:
        TAG_TAG.add(k)

NAME_KEYWORD = {}
NAME_RANK = {}
for _name, name, rank in name_rank():
    if rank < 3:
        continue
    name_list = [name[0]]
    name_tag_list = []
    for i in name[1:]:
        i = i.replace('#', '.').replace('[', '#').replace(']', '#')
        if i in TAG_TAG:
            name_tag_list.append(i)
        else:
            name_list.append(i)


    name = ' '.join((
        ' / '.join(name_list),
#        ' '.join('#%s#'%i for i in name_tag_list)
    )).strip()

    NAME_KEYWORD[name] = []
    for i in name_list:
        i = i.replace("·"," ")
        i = i.split()
        NAME_KEYWORD[name].extend(i)

#    NAME_RANK[name] = rank
    NAME_RANK[_name] = name

import _env
from zkit.pprint import pprint
from yajl import dumps

#pprint(NAME_KEYWORD)
#print dumps(NAME_KEYWORD)
print dumps(NAME_RANK)


