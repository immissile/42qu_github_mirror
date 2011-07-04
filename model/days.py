#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time, mktime, strptime, strftime
import datetime

DAY_SECOND = 3600 * 24
TIMEZONE_OFFSET = mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))

def today_days():
    return int(time()/DAY_SECOND)

def date_to_days(s):
    n = strptime(s, '%Y%m%d')
    seconds = mktime(n) - TIMEZONE_OFFSET
    return int(seconds / DAY_SECOND)

def yesterday():
    r = datetime.date.today()- datetime.timedelta(1)
    return r.strftime('%Y%m%d')

if __name__ == '__main__':
    print date_to_days('20110704')
    print yesterday()
