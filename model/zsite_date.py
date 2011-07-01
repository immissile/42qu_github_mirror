import datetime

START = datetime.date(1970,1,1)

def now_days():
    now = datetime.date.today()
    now_days = now - START
    return now_days.days

def zdate(days):
    i = datetime.timedelta(days) + START
    return i

