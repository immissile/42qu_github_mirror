import _env
from urllib2 import urlopen
from zkit.bot_txt import txt_wrap_by_all
from zkit.cn import has_cn

passed = set()
buffer = set(["108902385228996324856"])

touch = "http://42qu.com/google_plus?q="

while buffer:
    uid = buffer.pop()
    passed.add(uid)
    html = urlopen("https://plus.google.com/%s/posts?hl=en"%uid).read()
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
            urlopen(touch + str(i))

