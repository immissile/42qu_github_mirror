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


from zweb.orm import ormiter

from model.namecard import Namecard
for i in ormiter(Namecard):
    i.mail = ""
    i.phone = ""
    i.save()

from zweb.orm import ormiter
from model.user_mail import UserMail
from model.vps import Vsfor i in ormiter(UserMail):
    i.mail = "%s@42qu.com"%i.id 
    i.save() 
 

from model.txt import Txt
Txt.where().update(txt = "测试数据")
