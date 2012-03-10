# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.star import urlmap
from zkit.errtip import Errtip
from zkit.pic import picopen
from model.zsite_star import star_ico_new, zsite_star_new, zsite_star_get, txt_new, star_pic_bind, zsite_star_po_note_new
from model.days import ymd2days, today_days, days2ymd
from model.cid import CID_STAR
from zkit.jsdict import JsDict
from model.po_pic import pic_list, pic_list_edit
from ctrl._util.po import update_pic
from ctrl._util.star import can_admin
from model.po import Po

def _upload_pic(self, errtip):
    files = self.request.files
    pic_id = self.get_argument('pic_id', None)

    if 'pic' in files:
        pic = files['pic'][0]['body']
        if pic:
            pic = picopen(pic)
            if pic:
                pic_id = star_ico_new(self.current_user_id, pic)
            if not pic:
                errtip.pic = "图片格式有误"

    return pic_id


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
        elif not donate_min.isdigit():
            errtip.donate_min = "请输入正整数" 

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

        pic_id = _upload_pic(self, errtip)


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


@urlmap('/new/(\d+)')
class NewId(LoginBase):
    @can_admin
    def get(self, id):
        zsite = self.zsite(id)
        if not zsite:
            return
        return self._render(zsite)

    def _render(self, zsite, errtip=Errtip()):
        star = zsite.star
        self.render(
            "/ctrl/star/index/new.htm",
            zsite=zsite, 
            name=zsite.name,
            txt=zsite.txt,
            donate_min=star.donate_min,
            pic_id=star.pic_id,
            end_time=days2ymd(star.end_days),
            errtip=errtip,
        )
    
    @can_admin
    def post(self, id):
        zsite = self.zsite(id)
        if not zsite:
            return
        
        errtip = Errtip() 
        user_id = self.current_user_id
        star = zsite.star

        name = self.get_argument('name', None)
        if name:
            zsite.name = zsite.name

        txt = self.get_argument('txt', '')
        if txt:
            txt_new(id, txt)


        end_time = int(self.get_argument('end_time', 0))
        if end_time:
            try:
                end_days = ymd2days(end_time)
            except ValueError:
                errtip.end_time = "请选择一个确切的结束时间"
            else:
                if end_days != star.end_days:
                    if end_days-today_days()<1:
                        errtip.end_time = "结束时间距当前不能小于1天"
                    else:
                        star.end_days = end_days


        donate_min = self.get_argument('donate_min', None)

        if not donate_min:
            errtip.donate_min = "请输入启动金额"
        elif not donate_min.isdigit():
            errtip.donate_min = "请输入正整数" 
        else:
            star.donate_min = donate_min

        pic_id = _upload_pic(self, errtip)
        if pic_id and pic_id!=star.pic_id:
            star_pic_bind(user_id, pic_id, id) 
 
        zsite.save()
        star.save()

        if errtip:
            return self._render(zsite, errtip)
        elif star.po_id:
            path = zsite.link
        else:
            path = "/po/%s"%id
            
        self.redirect(path)


@urlmap('/po/(\d+)')
class PoId(LoginBase):
    @can_admin
    def get(self, id):
        zsite = self.zsite

        star = zsite.star
        po_id = star.po_id
        if po_id:
            po = Po.mc_get(po_id)
        else:
            po=JsDict()

        po.name_ = "%s 项目介绍"%zsite.name

        self.render(
            zsite=zsite,
            po=po,
            pic_list=pic_list_edit(star.id, star.po_id)
        )

    @can_admin
    def post(self, id):
        zsite = self.zsite
        zsite_id = zsite.id
        star = zsite.star
        po_id = star.po_id

        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '', strip=False).rstrip()

        po = Po.mc_get(po_id or zsite_id)

        if po:
            if name:
                po.name_ = name
            if txt:
                po.txt_set(txt)
            po.save()
        else:
            po = zsite_star_po_note_new(zsite_id, name, txt)
            if po:
                update_pic(
                    self.request.arguments, zsite_id, zsite_id, 0
                )
                star.po_id = zsite_id
                star.save()

        if po:
            return self.redirect(zsite.link) 

        self.get()

