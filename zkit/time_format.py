#!/usr/bin/env python
#coding:utf-8
from datetime import datetime

def friendly_hour(hour, minute=None, second=None):
    if 0 <= hour < 6:
        hour_str = "凌晨%s点"%hour
    elif 6 <= hour < 9:
        hour_str = "早上%s点"%hour
    elif 9 <= hour < 12:
        hour_str = "上午%s点"%hour
    elif hour == 12:
        hour_str = "中午"
    elif 12 < hour < 18:
        hour_str = "下午%s点"%(hour-12)
    elif 18 <= hour <= 24:
        hour_str = "晚上%s点"%(hour-12)
    t = [hour_str]
    if minute:
        t.append("%s分"%minute)
    else:
        t.append("整")
    return "".join(t)

def time_title():
    now = datetime.now()
    return "%s年%s月%s日 %s"%(
        now.year,
        now.month,
        now.day,
        friendly_hour(now.hour, now.minute, now.second)
    )


if __name__ == "__main__":
    print time_title()
