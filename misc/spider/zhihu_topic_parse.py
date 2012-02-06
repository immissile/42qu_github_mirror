#coding:utf-8

from zhihu_topic_data import ZHIHU_TOPIC
from collections import defaultdict

NAME_COUNT = defaultdict(int)

def name_rank():
    for id, name , url , img, rank in ZHIHU_TOPIC:
        id = int(id)
        if id == 6: #知乎指南
            continue
        if id == 96: #知乎产品改进
            continue
        name = [
            i.replace('）', '')
            for i in
            name.split('（')
        ]
        yield name, rank

for name, rank in name_rank():
    for i in name:
        NAME_COUNT[i] += 1

TAG_TAG = set()
for k, v in NAME_COUNT.iteritems():
    if v > 3:
        TAG_TAG.add(k)

for name, rank in name_rank():
    name_list = []
    name_tag_list = []
    for i in name:
        i = i.replace("/","|").replace("#",".").replace("[","#").replace("]","#")
        if i in TAG_TAG:
            name_tag_list.append(i)
        else:
            name_list.append(i) 


    name = " ".join((
        " / ".join(name_list),
        " ".join("#%s#"%i for i in name_tag_list)
    ))
    print name



if __name__ == '__main__':
    pass



