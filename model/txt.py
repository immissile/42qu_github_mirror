#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import  Model, cursor_by_table
from time import time

class Txt(Model):
    pass

def txt_set(id, txt):
    txt = txt.rstrip()
    t = Txt.get(id)
    if t is None:
        Txt(id=id, txt=txt).save()
    elif txt != t.txt:
        c = cursor_by_table('txt_history')
        c.execute(
            "insert into txt_history (rid,txt,create_time) values (%s,%s,%s)",
            (id, t.txt, int(time()))
        )
        c.connection.commit()
        t.txt = txt
        t.save()

def txt_get(id):
    c = Txt.raw_sql('select txt from txt where id=%s', id)
    r = c.fetchone()
    if r:
        return r[0]
    return ''

if __name__ == "__main__":
    from gid import gid
    id = 1#gid()
    txt_set(id, "test3")
    print txt_get(id)


