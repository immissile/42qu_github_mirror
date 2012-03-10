# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.star import urlmap
from zkit.errtip import Errtip
from zkit.pic import picopen
from model.zsite_star import star_ico_new, zsite_star_new
from model.days import ymd2days, today_days


@urlmap('/')
class Index(Base):
    def get(self):
        self.render()

@urlmap('/new')
class New(LoginBase):
    def get(self):
        self.render(errtip=Errtip())

    def post(self):
        errtip=Errtip()
        user_id = self.current_user_id

        name = self.get_argument('name', None)
        if not name:
            errtip.name = "请输入名称"

        donate_min = self.get_argument('donate_min', None)

        if not donate_min:
            errtip.donate_min = "请输入启动金额"

        end_time = int(self.get_argument('end_time', 0))
        if end_time:
            try:
                end_days = ymd2days(end_time)
            except ValueError:
                errtip.end_time = "请选择一个确切的结束时间"
            else:
                if end_days-today_days()<1:
                    errtip.end_time = "结束时间距当前不能小于1天"
 
        else:
            errtip.end_time = "请输入结束日期"


        txt = self.get_argument('txt', '')
        files = self.request.files

        pic_id = self.get_argument('pic_id', None)
        if 'pic' in files:
            pic = files['pic'][0]['body']
            if pic:
                pic = picopen(pic)
                if pic:
                    pic_id = star_ico_new(user_id, pic)
                if not pic:
                    errtip.pic = "图片格式有误"

        if not errtip.pic and not pic_id:
            errtip.pic = "请上传图片"


        if errtip:
            self.render(
                pic_id = pic_id,
                errtip = errtip,
                name = name,
                donate_min = donate_min,
                txt = txt,
                end_time = end_time
            )
        else:
            zsite = zsite_star_new(
                user_id, 
                name,  
                txt, 
                donate_min, 
                end_days, 
                pic_id
            )
            self.redirect("/po/%s"%zsite.id)


