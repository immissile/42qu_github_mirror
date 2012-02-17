#coding:utf-8

import _env
from glob import glob
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all

def parse_content(txt):
    id = txt_wrap_by('<a href="/question/', '/log" class="xrv">', txt)
    t = txt_wrap_by('<title>', ' - 知乎</title>', txt)
    tlist = txt_wrap_by_all('<div class="xmrw">', '</div>', txt)
    print id
    for i in tlist:
        print i
    raw_input() 





filelist = glob('/tmp/www.zhihu.com/*')

for i in filelist:
    with open(i) as f:
        t = f.read()
        if '<h3>邀请别人回答问题</h3>' in t:
            parse_content(t)

if __name__ == '__main__':
    pass



