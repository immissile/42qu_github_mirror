#coding:utf-8
import socket
hostname = socket.gethostname()
if hostname != 'e1':
    raise 'hostname is not e1'

import _env
import config
import config.host.e1
config.host.e1.prepare(config)
config.default.finish(config)

if config.MYSQL_HOST != "127.0.0.1":
    raise



from model.txt import Txt
from zweb.orm import ormiter
print Txt.get(10098265).txt

#for i in ormiter(Txt):
#    if "测试数据" in i.txt:
#        print i.txt 
#Txt.where().update(txt="测试数据")
#for i in ormiter(Txt):
#    print i.txt
