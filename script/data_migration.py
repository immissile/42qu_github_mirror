#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qu.myconf.config import KV_PATH

from zpage.model.fs import fs_file

from os import walk, makedirs
from os.path import join, getsize, splitext, exists, dirname
from shutil import copy

for prefix in ('0', '721', '470', '219'):
    for root, dirs, files in walk(join(KV_PATH, 'pic_show', prefix)):
        for name in files:
            opath = join(root, name)
            id = splitext(name)[0]
            if id.isdigit():
                id = int(id)
                path = fs_file(prefix, id, 'jpg')
                if not exists(path):
                    dirpath = dirname(path)
                    if not exists(dirpath):
                        makedirs(dirpath)
                    copy(opath, path)
