#coding:utf-8
import _env
from zhihu_topic_data_with_follow import ZHIHU_TOPIC
from collections import defaultdict
from model.zsite import Zsite
from model.cid import CID_TAG

NAME_COUNT = defaultdict(int)

def name_rank():
    for id, _name , url , img, rank in ZHIHU_TOPIC:
        name = _name
        id = int(id)
        if '知乎' in name and '知乎' != name:
            continue
        name = name.replace('|', '-')
        name = [
            i.replace('）', '')
            for i in
            name.split('（')
        ]
        yield id, _name , name, rank

for id, _name, name, rank in name_rank():
    for i in name:
        NAME_COUNT[i] += 1

TAG_TAG = set()
for k, v in NAME_COUNT.iteritems():
    if v > 3:
        TAG_TAG.add(k)

NAME_ID = {}
NAME_KEYWORD = {}
NAME_RANK = {}
for id, _name, name, rank in name_rank():
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

    name = name.replace(' I/O', 'IO').replace('TCP/IP', 'TCP-IP')


    NAME_ID[name] = id
    for i in map(str.strip,name.split("/")):
        if i not in NAME_ID:
            NAME_ID[i] = id

#    NAME_KEYWORD[name] = []
#    for i in name_list:
#        i = i.replace("·"," ")
#        i = i.split()
#        NAME_KEYWORD[name].extend(i)

#    NAME_RANK[name] = rank
#    if _name != name:
#        NAME_RANK[_name] = name

count = 0

MY2Z = {}
for i in Zsite.where(cid=CID_TAG):
    i.name = i.name.strip()
    i.save()
    if i.name not in NAME_ID:
        for j in map(str.strip,i.name.split("/")):
            if j in NAME_ID:
                MY2Z[i.id] = NAME_ID[j] 
                break
    else:
        MY2Z[i.id] = NAME_ID[i.name]
    if i.id not in MY2Z:
        count += 1
        #print count, '%s|'%i.name

import _env
from zkit.pprint import pprint
from yajl import dumps

pprint(dict((v,k) for k,v in MY2Z.iteritems()))
#print dumps(NAME_KEYWORD)
#print dumps(NAME_RANK)


