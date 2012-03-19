#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from time import time
from fs import fs_set_jpg, fs_url_jpg
from cid import CID_ICO, CID_ICO96, CID_PIC
from mail import rendermail


class PicMixin(object):
    def __getattr__(self, name):
        if name.startswith('src'):
            size = name[3:]
            if size.isdigit():
                return fs_url_jpg(size, self.id)


class Pic(Model, PicMixin):
    pass


def pic_new(cid, user_id):
    pic = Pic(
        cid=cid,
        user_id=user_id,
        create_time=int(time()),
    ).save()
    return pic.id

def pic_save(pic_id, pic):
    fs_set_jpg('0', pic_id, pic)



def pic_new_save(cid, user_id, pic):
    pic_id = pic_new(cid, user_id)
    pic_save(pic_id, pic)
    return pic_id


def pic_yes(id, admin_id):
    pic = Pic.get(id)
    if pic:
        pic.admin_id = admin_id
        pic.state = 1
        pic.save()

def _pic_no(id, admin_id):
    from ico import ico, ico96
    pic = Pic.get(id)
    if pic:
        pic.admin_id = admin_id
        pic.state = 0
        pic.save()
        cid = pic.cid
        #print pic.cid
        if cid == CID_ICO:
            user_id = pic.user_id
            if ico.get(user_id) == pic.id:
                ico.set(user_id, 0)
                ico96.set(user_id, 0)
        mq_pic_rm_mail(id)
        return user_id

def pic_no(id, admin_id):
    user_id = _pic_no(id, admin_id)
    if user_id:
        from zsite_show import zsite_show_rm
        from zsite_verify import zsite_verify_ajust
        from model.zsite import Zsite
        zsite = Zsite.mc_get(user_id)
        zsite_verify_ajust(zsite)

PIC_RM_TEMPLATE = {
    CID_ICO: '/mail/pic/rm_ico.txt',
}

def pic_rm_mail(id):
    from ico import ico
    from user_mail import mail_by_user_id
    from zsite import Zsite
    pic = Pic.get(id)
    if pic:
        cid = pic.cid
        user_id = pic.user_id
        template = PIC_RM_TEMPLATE.get(cid)
        if template:
            user = Zsite.mc_get(user_id)
            name = user.name
            mail = mail_by_user_id(user_id)
            if cid == CID_ICO:
                if not ico.get(user_id):
                    rendermail(
                       template,
                       mail,
                       name,
                       user=user,
                    )



from mq import mq_client
mq_pic_rm_mail = mq_client(pic_rm_mail)

if __name__ == '__main__':
    #for i in  Pic.where(user_id=10005704):
        #print i.id, i.cid
    from ico import ico
    print ico.get(10000645)
    ico.set(10000645,788)



