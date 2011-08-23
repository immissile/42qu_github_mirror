#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from model.kv_misc import kv_int_call, KV_EVENT_READY
from model.mail import rendermail
from zkit.single_process import single_process

@single_process
def main():
    title = [
        "线下活动 . 周报" 
    ]

    #先取城市 , 如没有活动 , 再取省份
    event_incr = 3
    
    if event_incr:
        place = "北京"
        title.append(
            "%s +%s 活动 "%(place, event_incr)
        )

    title = " . ".join(title)

    mail = "zsp009@gmail.com"
    name = "张沈鹏"

    rendermail(
        '/mail/event/weekly.htm', 
        mail, 
        name,
        format='html',
        subject=title
    )

if __name__ == '__main__':
    main()
