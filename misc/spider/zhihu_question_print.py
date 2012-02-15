#coding:utf-8
import _env
from zhihu_question_order_by_answer import QUESTION_LIST
from json import dumps, loads

for i in QUESTION_LIST:
    i = list(i)
    count , url, title, tags, txt = i
    if count == len(txt):
        for j in i[-1]:
            print j
            print loads(j.replace("\n",r"\n"))
        #i[-1] = map(loads,i[-1])
        #print dumps(i)

if __name__ == "__main__":
    pass



