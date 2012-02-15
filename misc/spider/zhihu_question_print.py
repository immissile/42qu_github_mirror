#coding:utf-8
import _env
from zhihu_question_order_by_answer import QUESTION_LIST

for count , url, title, tags in QUESTION_LIST:
    if count > 1:
        print count, url, title, "|"," ".join(tags)


if __name__ == "__main__":
    pass



