#coding:utf-8

from zhihu_topic_data import ZHIHU_TOPIC
from collections import defaultdict

NAME_COUNT = defaultdict(int)

def name_rank():
    for id, name , url , img, rank in ZHIHU_TOPIC:
        id = int(id)
        if id == 6: #知乎指南
            continue    
        name = [
            i.replace('）','') 
            for i in 
            name.split("（")
        ]
        yield name, rank

for name, rank in name_rank(): 
    for i in name:
        NAME_COUNT[i]+=1 


for name, rank in name_rank():
    for i in name:
        if NAME_COUNT[i]>2:
            print i, NAME_COUNT[i]

if __name__ == "__main__":
    pass



