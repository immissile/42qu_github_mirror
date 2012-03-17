#coding:utf-8
from json import loads
from datetime import datetime
import _env
from model.days import time_by_string
from model._db import Model


class SpiderWm(Model):
    pass


def wm_save(id, like, name, author, link, time, txt):
    if SpiderWm.get(wmid=id):
        return 

    now = datetime.today()

    id, like, name, author, link, time, txt = loads(line)
    if '前' in time:
        time = now
    else:
        time = time_by_string(time)

    like = int(like or 0)

    wm = SpiderWm(
        wmid=id,
        like=like, name=name, author=author, link=link, time=time, txt=txt
    )
    wm.save()

if __name__ == '__main__':
    pass



