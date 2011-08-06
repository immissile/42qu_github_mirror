# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_event import po_event_new
from zkit.errtip import Errtip
from zkit.jsdict import JsDict
from zkit.earth import pid_city 


@urlmap('/po/event')
@urlmap('/po/event/(\d+)')
class Index(LoginBase):
    def post(self, po_id=0):
        errtip = Errtip()
        address = self.get_argument('address', None)
        limit_up = self.get_argument('limit_up', "42")
        limit_down = self.get_argument('limit_down', "0")
        transport = self.get_argument('transport', '')
        price = self.get_argument('price','0')
        phone = self.get_argument('phone','')
        review = bool(self.get_argument('review',False))
        pid = self.get_argument('pid','1')

        if not pid.isdigit():
            errtip.pid = "请选择地址"

        pid = int(pid)
        pid2 = pid_city(pid)
        if not pid2: 
            errtip.pid = "请选择地址"

        if price:
            try:
                price = float(price)
            except:
                errtip.price = "请输入有效的金额"
            if price<0:
                errtip.price = "金额必须大于零"
        else:
            price = 0

        if not limit_down.isdigit():
            limit_down = 0
        else:
            limit_down = int(limit_down)
        
        if not limit_up.isdigit():
            limit_up = 42
        else:
            limit_up = int(limit_up)

        if limit_down > limit_up:
            limit_up, limit_down = limit_down, limit_up
            

        if not address:
            errtip.address = "请输入详细地址"

        if not phone:
            errtip.phone = "请输入联系电话"

        return self.render(
            errtip=errtip,
            address=address,
            limit_up=limit_up,
            limit_down=limit_down,
            transport=transport,
            price=price,
            phone=phone,
            review=review,
            pid=pid,
        )

    def get(self):
        return self.render(errtip=JsDict())



