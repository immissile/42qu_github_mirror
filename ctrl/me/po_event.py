# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model.po import Po
from model.po_event import po_event_new
from zkit.pic import picopen
from zkit.errtip import Errtip
from zkit.jsdict import JsDict
from zkit.earth import pid_city 
from model.po_event import EVENT_CID
from model.days import today_ymd_int 

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
        event_cid = self.get_argument('event_cid', '')
        begin_time = self.get_argument('begin_time','')
        end_time = self.get_argument('end_time','')
        begin_time = self.get_argument('begin_time','')

        begin_time_hour = self.get_argument('begin_time_hour', '0')
        begin_time_minute = self.get_argument('begin_time_minute', '0')
        end_time_hour = self.get_argument('end_time_hour','0')
        end_time_minute = self.get_argument('end_time_minute','0')

        begin_time_hour = int(begin_time_hour)
        begin_time_minute = int(begin_time_minute)

        end_time_hour = int(end_time_hour)
        end_time_minute = int(end_time_minute)
        
        if begin_time_hour>23 or begin_time_hour<0:
            begin_time_hour = 10
        
        if end_time_hour>23 or end_time_hour<0:
            end_time_hour = 11
        
        if begin_time_minute>59 or begin_time_minute<0:
            begin_time_minute = 0
        
        if end_time_minute>59 or end_time_minute<0:
            end_time_minute = 30




        if begin_time:
            begin_time = int(begin_time)

        if end_time:
            end_time = int(end_time)


        if begin_time > end_time:
            end_time, begin_time = begin_time, end_time
        
        if begin_time < today_ymd_int():
            errtip.begin_time = "这个时间 , 属于过去"


        begin = begin_time*(60*24)+begin_time_hour*60+begin_time_minute
        end = end_time*(60*24)+end_time_hour*60+end_time_minute

        if not event_cid.isdigit():
            errtip.event_cid = "请选择类型"
        else:
            event_cid = int(event_cid)
            if event_cid not in EVENT_CID:
                errtip.event_cid = "请选择类型"

        if not pid.isdigit():
            errtip.pid = "请选择地址"
        else:
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
        
        files = self.request.files
        if 'pic' in files:
            pic = files['pic'][0]['body']
            pic = picopen(pic)
            if not pic:
                errtip.pic = "图片格式有误"
        else:
            errtip.pic = "请上传图片" 



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
            event_cid=event_cid,
            begin_time = begin_time,
            end_time = end_time,
            begin_time_hour = begin_time_hour,
            begin_time_minute = begin_time_minute,
            end_time_hour = end_time_hour,
            end_time_minute = end_time_minute,
        )

    def get(self):
        return self.render(errtip=JsDict())



