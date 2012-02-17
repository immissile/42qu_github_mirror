#coding:utf-8

import _env
from json import dumps, loads
from zhihu_topic_data_with_follow import ZHIHU_TOPIC
from zkit.pprint import pprint
from name2id import NAME2ID
from zdata.tag.name_tidy import name_tidy
from zhihu_topic_url2id import ID2MY
from itertools import chain
from zhihu_question_load import zhihu_to_dump

id2topic = dict([(i[1], i[0]) for i in ZHIHU_TOPIC])

myidset = set(NAME2ID.itervalues())
myiddict = dict([(k, v) for v, k in NAME2ID.iteritems()])

def tag_id_list_by_str_list(tags):
    tag_list = []

    for tag in tags:
        id = tag_to_id(tag)
        if not id:
            continue
        else:
            tag_list.append(id)

    return tag_list

def tag_to_id(tag):
    tag = str(tag)
    id = id2topic.get(tag, 0)
    if id in ID2MY:
        id = ID2MY[id]
        if id not in myidset:
            id = 0
    else:
        id = 0

    if not id:
        tag = name_tidy(tag)
        id = NAME2ID.get(tag, 0)
    return id

def txt_tag(filename):
    with open(filename) as zhihu_question_dump:
        for line in zhihu_question_dump:
            line = loads(line)
            yield line[-2], line[2], line[-1]

        #    tag_list = tag_id_list_by_str_list(line[-2])
        #    yield line[2], tag_list
        #    for t in line[-1]:
        #        yield t, tag_list


def txt_tag_id_list():
    txt_list = []

    for tag_string , title, _txt_list in chain(
        zhihu_to_dump(),
        txt_tag('zhihu_question_to_dump.json'),
    ):
        tag_list = tag_id_list_by_str_list(tag_string)

        txt_list.append(title)
        txt_list.extend(_txt_list)
        yield tag_list, txt_list

if __name__ == '__main__':
    pass

    for tag_list, txt_list in txt_tag_id_list():
        print tag_list 

#    for i in :
#        yield i[0], i[]

        #yield line[2], tag_list
        #for t in line[-1]:
        #    yield t, tag_list
        #for tag in tag_string:
        #    print tag


#        print txt
#        for i in tag_list:
#            print myiddict[i],
#        print '\n'



