#coding:utf-8
from json import loads
from datetime import datetime
import _env
from model.days import time_by_string
from model._db import Model


class SpiderWm(Model):
    pass


now = datetime.today()

with open('wm_rec.txt') as wm_rec:
    for line in wm_rec:
        id, like, name, author, link, time, txt = loads(line)
        if '前' in time:
            time = now
        else:
            time = time_by_string(time)

        like = int(like or 0)
        if SpiderWm.get(wmid=id):
            continue
        print id, name

        wm = SpiderWm(
            wmid=id,
            like=like, name=name, author=author, link=link, time=time, txt=txt
        )
        wm.save()

if __name__ == '__main__':
    pass



