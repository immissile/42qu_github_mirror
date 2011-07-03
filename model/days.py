from time import time

DAY_SECOND = 3600*24

def today_days():
    return int(time()/DAY_SECOND)


