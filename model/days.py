#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time, mktime, strptime, strftime
import datetime

ONE_DAY = 3600 * 24
TIMEZONE_OFFSET = mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))

def today_seconds():
    return int(time()/ONE_DAY)*ONE_DAY

def today_days():
    return int(time()/ONE_DAY)


def yesterday_seconds():
    return today_days() - ONE_DAY

def date_to_days(s):
    n = strptime(s, '%Y%m%d')
    seconds = mktime(n) - TIMEZONE_OFFSET
    return int(seconds / ONE_DAY)


def yesterday():
    r = datetime.date.today()- datetime.timedelta(1)
    return r.strftime('%Y%m%d')


def today_year():
    return datetime.date.today().year


def year_month_str(date):
    year = date//10000
    result = [year]
    month = date%10000//100
    if month:
        result.append(month)
    return '.'.join(map(str, result))


def year_month_begin_end(begin, end):
    r = []
    if begin:
        r.append(begin)
    if end and end != begin:
        r.append(end)

    return ' - '.join(map(year_month_str, r))


TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def epoch_seconds(timestr):
    return int(mktime(strptime(timestr, TIMESTAMP_FORMAT)))


if __name__ == '__main__':
    #print date_to_days('')
    #print yesterday()
    #print today_year()
    #date = 20110704
    #print year_month_begin_end(date, date)
    print today_seconds()
