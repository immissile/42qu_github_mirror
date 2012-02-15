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


with open('zhihu_question_dumped.json') as zhihu_question_dump:
    for line in zhihu_question_dump:
        line = loads(line)
        tags = line[-2]
        for tag in tags:
            tag = str(tag)
            id = id2topic.get(tag, 0)
            if not id:
                tag = name_tidy(tag)
                id = NAME2ID.get(tag, 0)
            else:
                if id in ID2MY:
                    id = ID2MY[id]
                    print id
                    if id not in myidset:
                        id = 0
                else:
                    id = 0 
            if not id:
                print tag
                raw_input()
                continue

if __name__ == '__main__':
    pass



