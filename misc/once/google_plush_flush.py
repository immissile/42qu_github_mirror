import _env
from urllib2 import urlopen
from zkit.bot_txt import txt_wrap_by_all
from zkit.cn import has_cn
import sys
import traceback
import datetime

passed = set()
buffer = set(['104125703399587452620'])

touch = 'http://42qu.com/google_plus?q='

while buffer:
    uid = buffer.pop()
    passed.add(uid)
    url = 'https://plus.google.com/%s/posts?hl=en'%uid
    print url
    try:
        html = urlopen(url, timeout=60).read()
    except:
        traceback.print_exc()
        continue
    if not has_cn(html):
        continue

    for i in txt_wrap_by_all('href="/', '"', html):
        if i.isdigit():
            i = int(i)
            if i in passed:
                continue
            if i in buffer:
                continue
            buffer.add(i)
            print i, datetime.datetime.now()
            sys.stdout.flush()
            try:
                urlopen(touch + str(i), timeout=30)
            except:
                traceback.print_exc()
                continue
