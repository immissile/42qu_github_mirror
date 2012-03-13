#coding:utf-8
import socket
hostname = socket.gethostname()
if hostname != "e1":
    raise "hostname is not e1"


import _env
from model.txt import Txt
from zweb.orm import ormiter

Txt.where().update(txt="测试数据")
for i in ormiter(Txt):
    print i.txt
