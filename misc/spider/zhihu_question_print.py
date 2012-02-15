#coding:utf-8

import _env
from json import dumps, loads
from zhihu_topic_data_with_follow import ZHIHU_TOPIC
from zkit.pprint import pprint
from name2id import NAME2ID
from zdata.tag.name_tidy import name_tidy
from zhihu_topic_url2id import ID2MY

id2topic = dict([(i[1], i[0]) for i in ZHIHU_TOPIC])

myidset = set(NAME2ID.itervalues())

def txt_tag(): 
    with open('zhihu_question_dumped.json') as zhihu_question_dump:
        for line in zhihu_question_dump:
            line = loads(line)
            tags = line[-2]
            tag_list = []

            for tag in tags:
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

                if not id:
                    continue
                else:
                    tag_list.append(id)
            yield line[0], tag_list


if __name__ == '__main__':
    pass

    for txt, tag_list in txt_tag():
        print txt, tag_list
        


