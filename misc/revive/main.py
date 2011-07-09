#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env

from qu.myconf.config import KV_PATH

from zpage.model.fs import fs_file

from os import walk, makedirs
from os.path import join, getsize, splitext, exists, dirname
from shutil import copy

def ico_file_mv():
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

from zpage.model.ico import *
def ico96_regen():
    for id, value in ico.iteritems():
        if ico96.get(id):
            return

        pic = picopen(fs_get_jpg(PIC_FULL_SIZE, value))
        if not pic:
            return

        pic_id = pic_new(CID_ICO96, id)

        pos = ico_pos.get(id)

        if pos:
            pos_tuple = pos.split('_')
            if len(pos_tuple) == 3:
                try:
                    x, y, size = map(int, pos_tuple)
                except:
                    print pos_tuple
                    raise
                else:
                    if size:
                        pic = pic_square(pic, size, top_left=(x, y), size=size)

        pic = pic_square(pic, 96, size=96)
        fs_set_jpg('96', pic_id, pic)
        ico96.set(id, pic_id)

if __name__ == '__main__':
    ico_file_mv()
    ico96_regen()
