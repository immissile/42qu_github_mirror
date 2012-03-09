# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.star import urlmap
from zkit.errtip import Errtip
from zkit.pic import picopen

@urlmap('/')
class Index(Base):
    def get(self):
        self.render()

@urlmap('/new')
class New(Base):
    def get(self):
        self.render(errtip=Errtip())

    def post(self):
        errtip=Errtip()

        name = self.get_argument('name', None)
        donate_min = self.get_argument('donate_min', None)
        end_time = self.get_argument('end_time', None)
        txt = self.get_argument('txt', '')
        files = self.request.files

        if 'pic' in files:
            pic = files['pic'][0]['body']
            if pic:
                pic = picopen(pic)
            else:
                errtip.pic = "图片格式有误"
        else:
            errtip.pic = "请上传图片"

        if errtip:
            self.render(
                errtip = errtip,
                name = name,
                donate_min = donate_min,
                txt = txt,
                end_time = end_time
            )

