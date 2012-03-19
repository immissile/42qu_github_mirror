#!/usr/bin/env python
#coding:utf-8
from datetime import datetime, timedelta

def friendly_hour(hour, minute=None, second=None):
    if 0 <= hour < 6:
        hour_str = '凌晨%s点'%hour
    elif 6 <= hour < 9:
        hour_str = '早上%s点'%hour
    elif 9 <= hour < 12:
        hour_str = '上午%s点'%hour
    elif hour == 12:
        hour_str = '中午'
    elif 12 < hour < 18:
        hour_str = '下午%s点'%(hour-12)
    elif 18 <= hour <= 24:
        hour_str = '晚上%s点'%(hour-12)
    t = [hour_str]
    if minute:
        t.append('%s分'%minute)
    else:
        t.append('整')
    return ''.join(t)

def time_title():
    now = datetime.now()
    return '%s年%s月%s日 %s'%(
        now.year,
        now.month,
        now.day,
        friendly_hour(now.hour, now.minute, now.second)
    )

ONE_DAY = timedelta(days=1)

def friendly_time(mtime):
    mtype = type(mtime)
#    if mtype is str:
#        time = time_conv(mtime)
    if mtype is int or mtype is long or mtype is float:
        time = datetime.fromtimestamp(mtime)
    else:
        time = mtime

    if time is None:
        return mtime

    now = datetime.now()
    diff = now-time
    seconds = diff.seconds
    diff_days = diff.days
    if (time+timedelta(diff_days)).timetuple()[:3] != now.timetuple()[:3]:
        diff_days += 1

    if diff_days == 0 or (diff_days == 1 and seconds<21600):
        if seconds < 36000:
            if seconds < 3600:
                f = int(seconds/60)
                if f == 0:
                    if seconds:
                        return '%s秒前'%seconds
                    else:
                        return '刚刚'
                else:
                    return '%s分钟前' % f
            else:
                return '%s小时前' % int(seconds/3600)
        return friendly_hour(time.hour, time.minute, time.second)
    elif 0 < diff_days < 3:
        cc_time = ONE_DAY + time
        if now.day == cc_time.day:
            return '昨天 %s' % friendly_hour(time.hour, time.minute, time.second)
        elif now.day == (cc_time + ONE_DAY).day:
            return '前天 %s' % friendly_hour(time.hour, time.minute, time.second)

    if now.year == time.year:
        return '%s月%s日 %s' % (time.month, time.day, friendly_hour(time.hour, time.minute, time.second))
    else:
        return '%s年%s月%s日 %s'% (time.year, time.month, time.day, friendly_hour(time.hour, time.minute, time.second))




if __name__ == '__main__':
    from time import time
    print friendly_time(time()-100)
