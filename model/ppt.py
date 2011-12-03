#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from model.fs import fs_set, fs_path, fs_url, fs_file

class Ppt(Model):
    pass

def ppt_new(com_id, ppt):
    p = Ppt(com_id=com_id)
    p.save()
    fs_set("ppt",p.id,"ppt",ppt)
    return p.id

def ppt_file(id):
    return fs_file("ppt", id, "ppt")

if __name__ ==  "__main__":
    id = ppt_new(1,"12345")
    print ppt_file(id)



