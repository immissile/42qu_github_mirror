#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qu.myconf.config import KV_PATH

from zpage.model.fs import FS_PATH, fs_file
from zpage.model.pic import ico_save
from zpage.zkit.pic import picopen

from os import walk, makedirs
from os.path import join, getsize, splitext, exists, dirname
from shutil import copy

for root, dirs, files in walk(join(KV_PATH, 'pic_show', '0')):
    for name in files:
        opath = join(root, name)
        id = splitext(name)[0]
        if id.isdigit():
            id = int(id)
            path = fs_file('0', id, 'jpg')
            if not exists(path):
                dirpath = dirname(path)
                if not exists(dirpath):
                    makedirs(dirpath)
                copy(opath, path)

for root, dirs, files in walk(join(FS_PATH, '0')):
    for name in files:
        path = join(root, name)
        id = splitext(name)[0]
        id = int(id)
        with open(path) as f:
            ico_save(id, picopen(f))
