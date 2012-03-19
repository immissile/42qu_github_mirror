URL = "http://huaban.com/boards/%s/?limit=999999"
BEGIN = 0 
MAX = 399999

import urllib2
from json import loads,dumps
import traceback

def fetch_board(i):
    url = URL%i
    req = urllib2.Request(url)
    req.add_header('X-Request', 'JSON')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    r = urllib2.urlopen(req)
    json = r.read()
    data = loads(json)
#    raise
    if 'board' in data:
        count = data['board']['pin_count']
        if count:
            #print dumps(data)
            print i, count 
            return dumps(data)

with open("/mnt/zdata/data/huaban.js","w") as huaban:
    for i in xrange(BEGIN, MAX):
        try:
            r = fetch_board(i)
        except:
            traceback.print_exc()
            continue            
        if r:
            huaban.write(r+"\n")
            huaban.flush()

