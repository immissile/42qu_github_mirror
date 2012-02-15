#coding:utf-8
import _env
from json import dumps, loads
from zhihu_topic_data_with_follow import ZHIHU_TOPIC
from zkit.pprint import pprint
from name2id import NAME2ID
from zdata.tag.name_tidy import name_tidy

id2topic = dict([(i[1], i[0]) for i in ZHIHU_TOPIC])

with open('zhihu_question_dumped.json') as zhihu_question_dump:
    for line in zhihu_question_dump:
        line = loads(line)
        tags = line[-2]
        for tag in tags:
            tag = str(tag)
            id = id2topic.get(tag,0)
            if not id:
                tag = name_tidy(tag)
                id = NAME2ID.get(tag, 0)
            else:
                pass
            print id
            if not id:
                print tag
                raw_input() 

if __name__ == '__main__':
    pass



