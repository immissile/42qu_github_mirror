#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from time import time
from fs import fs_set_jpg, fs_url_jpg

class Pic(Model):
    pass

def pic_new(tid, user_id):
    p = Pic(
        tid=tid,
        user_id=user_id,
        create_time=int(time()),
    ).save()
    return p.id

def pic_save(pic_id, pic):
    fs_set_jpg('0', pic_id, pic)
