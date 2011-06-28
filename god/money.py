#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.money import withdraw_list, Trade 
from model.mail import sendmail


@urlmap('/withdraw')
class WithDraw(Base):
    def get(self):
        self.render( withdraw_list = withdraw_list())

    def post(self):
        id = self.get_argument('id','').strip()
        body = self.request.body
        if "reject=" in body:
            i = Trade.get(id)
            cid = i.cid 
            txt = "%s 提现失败"%cid   
            withdraw_fail(id,txt)
            
            mail = mail_by_user_id(id)
            message = "\n".join((
"请求提现金额: %s"%(i.price/100.0),
"%s账号: %s"%(i.payname, i.account),
"%s姓名: %s"%(i.payname, i.name),
"请检查设置的 %s 账号/姓名 是否正确 , 然后重新提交提现请求"%(i.payname),
"如果有问题或疑问, 请发邮件到 %s"%HELP_EMAIL
                    ))
            sendmail('42qu'.txt, message, mail, i.name)
        else:
            trade_no = self.get_argument('trade_no','').strip()
            if trade_no:
                trade = Trade.get(id)
                trade.finish()
                return self.get()

