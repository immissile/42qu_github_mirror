#!/usr/bin/env python
#coding:utf-8
import _env
import re
from cgi import escape
from config import SITE_DOMAIN
from zkit.bot_txt import  txt_wrap_by, txt_map
from uuid import uuid4
from model.video_swf import video_autoplay_link, _HTM_SWF

RE_LINK = re.compile(
r'((?:https?://[\w\-]+\.)'
r'[\w\-.%/=+#:~!,\'\*\^@]+'
r'(?:\?[\w\-.;%/=+#:~!,\'\*&$@]*)?)'
)
RE_LINK_TARGET = re.compile(
r'(\[\[)?((?:https?://[\w\-]+\.)'
r'[\w\-.%/=+#:~!,\'\*\^@]+'
r'(?:\?[\w\-.;%/=+#:~!,\'\*&$@]*)?)(\]\])?'
)
RE_SPACE = re.compile(""" ( +)""")
RE_AT = re.compile(r'(\s|^)@([^@\(\)\s]+(?:\s+[^@\(\)\s]+)*)\(([a-zA-Z0-9][a-zA-Z0-9\-]{,31})\)(?=\s|$)')
RE_BOLD = re.compile(r'\*{2}([^\*].*?)\*{2}')
RE_CODE = re.compile(r'\{\{\{(.*)\}\}\}', re.S)
RE_IMG = re.compile(r'图://(.+?(jpg|gif|png|jpeg))')


def replace_space(match):
    return ' '+len(match.groups()[0])*'&nbsp;'


class ReplaceCode(object):
    def __init__(self):
        self._u2s = {}

    def __call__(self, txt):
        coding = txt[1:-1].replace('\r', '\n')
        pos = coding.find('\n')
        typ = coding[3:pos]
        if typ.startswith('#!'):
            typ = typ[2:]
            if typ in ('c', 'c++'):
                typ = 'cpp'
        else:
            typ = ''
        coding = coding[pos:coding.rfind('\n')]
        if typ:
            builder = '<pre class="codebrush brush: %s" type="syntaxhighlighter">%s</pre>'%(typ, coding)
        else:
            builder = '<pre>%s</pre>'%coding
        builder = '<div class="codesh">%s</div>'%builder

        uuid = uuid4().hex
        self._u2s[uuid] = builder

        return uuid

    def loads(self, txt):
        for k, v in self._u2s.iteritems():
            txt = txt.replace(k, v)
        return txt

def replace_link(match):
    gs = match.groups()
    b, g , e = gs
    video = video_autoplay_link(g)

    if video:
        return '<a onclick="fdvideo(this);" class="fdvideo" href="%s">播放视频</a>'%g
    elif g.endswith('.swf'):
        return _HTM_SWF%g
    else:
        if (b and b.startswith('[[')) and (e and e.endswith(']]')):
            return """<a title="%s" target="_blank" href="%s" class="aH" rel="nofollow"></a>""" %(g, g)
        else:
            return """<a target="_blank" href="%s" rel="nofollow">%s</a>""" %(g, g)
    return ''

def replace_img(match):
    g = match.groups()[0]
    return """<img src="//%s">""" %g

def replace_bold(match):
    txt = match.groups()[0]
    return '<b>%s</b>' % txt.strip()

def txt_withlink(s):
    if type(s) is unicode:
        s = str(s)
    s = '\r'.join(map(str.rstrip, s.replace('\r\n', '\r').replace('\n', '\r').split('\r')))
    s = escape(s)
    replace_code = ReplaceCode()
    s = txt_map('\r{{{', '\r}}}\r', '\r%s\r'%s, replace_code).strip()
    s = RE_BOLD.sub(replace_bold, s)

    s = replace_link_img(s)

    s = RE_AT.sub(replace_at, s)
    s = replace_code.loads(s)

    return s

def replace_link_img(s):
    s = s.replace('图：', '图:')
    s = s.replace('图: http://', '图:http://')
    s = s.replace('图:http://', '图://')

    s = RE_LINK_TARGET.sub(replace_link, s)

    s = RE_IMG.sub(replace_img, s)
    return s

def txt2htm_withlink(s):
    s = escape(s)
    s = s.replace('\n', '\n<br>')
    s = replace_link_img(s)
    s = RE_SPACE.sub(replace_space, s)
    return s

def replace_at(match):
    prefix, name, url = match.groups()
    return '%s@<a target="_blank" href="//%s.%s">%s</a>' % (prefix, url, SITE_DOMAIN, name)


if __name__ == '__main__':
    print """
<!doctype html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head>
<body>
%s
</body>
</html>
"""%txt_withlink(r'''
支付宝推荐
交通罚款代办全新上线！全国交通违章罚单免费查询。
出账单：全民年度账单发布，年度大盘点，《2011，我们一起走过》
更多帮助 | 去问吧找答案
图:http://img3.douban.com/lpic/s7044274.jpg  图:http://img3.douban.com/lpic/s704427411.jpg 
图:http://img3.douban.com/lpic/s7044274.jpg 
http://img3.douban.com/lpic/s7044274.jpg
    ''')

#    print txt_withlink( """
#{{{#!python
#/**
#s
#**/
#def replace_at(match):
#
#    prefix, name, url = match.groups()
#    return '%s@<a target="_blank" href="//%s.%s">%s</a>' % (prefix, url, SITE_DOMAIN, name)
#
#}}}""")

    print txt_withlink(r'''                                                        
支付宝推荐
图:http://img3.douban.com/lpic/s7044274.jpg  图:http://img3.douban.com/lpic/s704427411.jpg 
图:http://img3.douban.com/lpic/s7044274.jpg                                        
http://img3.douban.com/lpic/s7044274.jpg
xxx[[http://img3.douban.com/lpic/s7044274]]
    ''').decode('utf-8', 'ignore')

#    print txt_withlink("""
#输出 :
#Google Reader 视频
#http://player.youku.com/player.php/sid/XMjQ2ODM1Mjcy/v.swf
#加勒比海盗
#http://player.youku.com/player.php/sid/XMzA4NDkzNTQ4/v.swf
#""")
