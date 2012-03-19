#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import ZsiteBase, LoginBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase
from model.zsite_com import com_pic_new, zsite_com_new, pid_by_com_id, ZsiteCom, zsite_com_place_new
from model.po_video import video_new
from model.video_swf import video_filter
from zkit.pic import picopen
from zkit.errtip import Errtip
from model.ico import ico96
from model.motto import motto as _motto, motto_set
from model.ico import site_ico_new, site_ico_bind
from model.zsite_com import ZsiteCom
from model.gid import gid
from model.ppt import ppt_new

def _bio_save(self, edit=None):
    hope = self.get_argument('hope', '', False).rstrip()
    money = self.get_argument('money', '', False).rstrip()
    culture = self.get_argument('culture', '', False).rstrip()
    team = self.get_argument('team', '', False).rstrip()
    video = self.get_argument('video', '')
    com_id = self.zsite.id
    files = self.request.files
    cover_id = None

    if 'cover' in files:
        cover = files['cover'][0]['body']
        if cover:
            cover = picopen(cover)
            if cover:
                cover_id = com_pic_new(com_id, cover)

    for pic in files.get('pic', ()):
        if pic['body']:
            pic = picopen(pic['body'])
            if pic:
                com_pic_new(com_id, pic)

    if video:
        video_id = gid()
        video, video_site = video_filter(video)
        video_new(video_id, video)
    else:
        video_id = 0
        video_site = None

        ppt = files.get('ppt')
        if ppt:
            ppt = ppt[0]['body']
            ppt_new(com_id, ppt)

    zsite_com_new(com_id, hope, money, culture, team, cover_id, video_site, video_id)



@urlmap('/bio/edit')
class BioEdit(AdminBase):
    def get(self):
        zsite_com = ZsiteCom.mc_get(self.zsite_id)
        return self.render(
                '/ctrl/zsite/com/bio/bio_new.htm',
                edit=True,
                zsite_com=zsite_com,
                )

    _bio_save = _bio_save

    def post(self):
        self._bio_save(edit=True)
        self.redirect('/')



@urlmap('/bio/new')
class BioNew(AdminBase):
    def get(self):
        return self.render()

    _bio_save = _bio_save
    def post(self):
        self._bio_save()
        self.redirect('/job/new')


@urlmap('/guide')
class Guide(AdminBase):
    def get(self):
        self.render()

@urlmap('/bio/admin')
class BioAdmin(AdminBase):
    def get(self):
        errtip = Errtip()
        name = self.zsite.name
        com_id = self.zsite_id
        pic_id = ico96.get(com_id)
        motto = _motto.get(com_id)
        pid_add = pid_by_com_id(com_id)
        pid_add = [[i.pid, i.address] for i in pid_add]
        zc = ZsiteCom.mc_get(com_id)
        phone = None
        if zc:
            phone = zc.phone


        self.render(
                    '/ctrl/com/index/com_new.htm',
                    errtip=errtip,
                    motto=motto,
                    pic_id=pic_id,
                    name=name,
                    phone=phone,
                    pid_add=pid_add,
                    edit=True)


    def post(self):
        errtip = Errtip()
        current_user = self.current_user
        current_user_id = current_user.id
        name = self.get_argument('name', None)
        motto = self.get_argument('motto', None)
        pid = self.get_arguments('pid', None)
        address = self.get_arguments('address', None)
        phone = self.get_argument('phone', None)
        pid_add = zip(pid, address)
        zsite = self.zsite

        if not name:
            errtip.name = '请输入名称'
        else:
            zsite.name = name
            zsite.save()

        if not motto:
            errtip.motto = '请编写签名'



        files = self.request.files
        pic_id = None

        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if pic:
                pic_id = site_ico_new(current_user_id, pic)
            else:
                errtip.pic = '图片格式有误'
        else:
            pic_id = self.get_argument('pic_id', None)
            if not pic_id:
                errtip.pic = '请上传图片'


        if not errtip:
            current_user_id = self.current_user_id
            com_id = self.zsite_id
            zsite_com_new(com_id, phone=phone)
            site_ico_bind(current_user_id, pic_id, com_id)
            motto_set(com_id, motto)
            if pid_add:
                for pa in pid_add:
                    zsite_com_place_new(com_id, int(pa[0]), pa[1])
            else:
                pid_add = self.get_argument('pid_add', None)
            return self.redirect('/')


        return self.render(
            errtip=errtip,
            name=name,
            motto=motto,
            #txt=txt,
            phone=phone,
            pic_id=pic_id,
            pid_add=pid_add
        )

