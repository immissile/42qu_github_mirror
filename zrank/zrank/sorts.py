from zrank_sort import hot as _hot, confidence as _confidence


def hot(ups, downs, time):
    return int(_hot(ups + 1, downs, time) * 100)


SMALLINT = 1 << 16

def confidence(ups, downs):
    return int(_confidence(ups + 1, downs) * SMALLINT)
