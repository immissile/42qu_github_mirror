#coding:utf-8
from yajl import dumps

def json_encode(value):
    return dumps(value).replace("</", "<\\/")

if __name__ == "__main__":
    print json_encode("张沈鹏")


