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

from zpage.model.zsite import Zsite
from zpage.zweb.orm import ormiter

#def user_info():
#    from qu.mysite.model.man_profile import ManProfile
#    from zpage.model.user_info import user_info_new
#    for i in ormiter(Zsite):
#        id = i.id
#        mp = ManProfile.get(id)
#        if mp:
#            user_info_new(id, 0, 0, 0, mp.gender or 2)

def namecard():
    from qu.mysite.model.namecard import Namecard
    from zpage.model.namecard import namecard_new
    for i in ormiter(Namecard):
        u = Zsite.get(i.id)
        if u:
            namecard_new(i.id, i.pid, u.name, i.phone, i.mail, i.address)

def career():
    from qu.mysite.model.company import CompanyMan, CompanyBeginEnd, CompanyManTxt, company_man_by_man_id
    from zpage.model.career import career_set
    for i in ormiter(Zsite):
        id = i.id
        c_li = company_man_by_man_id(id)
        for c in c_li:
            career_set(0, id, c.com_name, c.title, c.txt, c.time.begin_time, c.time.end_time, c.cid or 1)

if __name__ == '__main__':
    ico_file_mv()
    ico96_regen()
    namecard()
    career()
