#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import  Model, cursor_by_table, McCache
from time import time


class Txt(Model):
    pass

def txt_new(id, txt):
    txt = txt.replace('\r\n', '\n').replace('\r', '\n').rstrip()
    t = Txt.get(id)
    if t is None:
        Txt(id=id, txt=txt).save()
    elif txt != t.txt:
        c = cursor_by_table('txt_history')
        c.execute(
            'insert delayed into txt_history (rid,txt,create_time) values (%s,%s,%s)',
            (id, t.txt, int(time()))
        )
        c.connection.commit()
        t.txt = txt
        t.save()
    mc_flush(id, txt)

mc_txt = McCache('Txt:%s')

@mc_txt('{id}')
def txt_get(id):
    c = Txt.raw_sql('select txt from txt where id=%s', id)
    r = c.fetchone()
    if r:
        return r[0]
    return ''

def txt_bind(o_list):
    r = mc_txt.get_multi(i.id for i in o_list)
    for i in o_list:
        iid = i.id
        txt = r[iid]
        if txt is None:
            i.txt = txt_get(iid)
        else:
            i.txt = txt

def mc_flush(id, txt=None):
    if txt is None:
        mc_txt.delete(id)
    else:
        mc_txt.set(id, txt)

if __name__ == '__main__':
    pass
