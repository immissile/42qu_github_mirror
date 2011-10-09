#!/usr/bin/env python
#coding:utf-8
import _env
import re
from cgi import escape
from config import SITE_DOMAIN
RE_LINK = re.compile(
r'((?:https?://[\w\-]+\.)'
r'[\w\-.%/=+#:~!,\'\*\^@]+'
r'(?:\?[\w\-.%/=+#:~!,\'\*&$@]*)?)'
)
RE_LINK_TARGET = re.compile(
r'(\[\[)?((?:https?://[\w\-]+\.)'
r'[\w\-.%/=+#:~!,\'\*\^@]+'
r'(?:\?[\w\-.%/=+#:~!,\'\*&$@]*)?)(\]\])?'
)
RE_SPACE = re.compile(""" ( +)""")
RE_AT = re.compile(r'(\s|^)@([^@\(\)\s]+(?:\s+[^@\(\)\s]+)*)\(([a-zA-Z0-9][a-zA-Z0-9\-]{,31})\)(?=\s|$)')
RE_BOLD = re.compile(r'\*{2}([^\*].*?)\*{2}')

HTM_SWF = """<embed src="%s" quality="high" class="video" allowfullscreen="true" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" wmode= "Opaque"></embed>"""
HTM_YOUKU = HTM_SWF%'''http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior'''

def replace_space(match):
    return ' '+len(match.groups()[0])*'&nbsp;'

def replace_link(match):
    gs = match.groups()
    b, g , e = gs
    if g.startswith('http://v.youku.com/v_show/id_'):
        g = g[29:g.rfind('.')]
        return HTM_YOUKU%g
    elif g.startswith('http://player.youku.com/player.php/sid/'):
        g = g[39:g.rfind('/')]
        return HTM_YOUKU%g
    elif g.endswith('.swf'):
        return HTM_SWF%g
    else:
        if (b and b.startswith('[[')) and (e and e.endswith(']]')):
            return """<a title="%s" target="_blank" href="%s" class="aH" rel="nofollow"></a>""" %(g, g)
        else:
            return """<a target="_blank" href="%s" rel="nofollow">%s</a>""" %(g, g)
    return ''

def replace_bold(match):
    txt = match.groups()[0]
    return '<b>%s</b>' % txt.strip()

def txt_withlink(s):
    s = escape(s)
    s = RE_BOLD.sub(replace_bold, s)
    s = RE_LINK_TARGET.sub(replace_link, s)
    s = RE_AT.sub(replace_at, s)
    return s

def txt2htm_withlink(s):
    s = escape(s)
    s = s.replace('\n', '\n<br>')
    s = RE_LINK_TARGET.sub(replace_link, s)
    s = RE_SPACE.sub(replace_space, s)
    return s

def replace_at(match):
    prefix, name, url = match.groups()
    return '%s@<a target="_blank" href="//%s.%s">%s</a>' % (prefix, url, SITE_DOMAIN, name)


if __name__ == '__main__':

    print txt_withlink( """
http://zuroc.42qu.com/live
[[http://zuroc.42qu.com/live]]

""")

#    print txt_withlink("""
#输出 :
#Google Reader 视频
#http://player.youku.com/player.php/sid/XMjQ2ODM1Mjcy/v.swf
#加勒比海盗
#http://player.youku.com/player.php/sid/XMzA4NDkzNTQ4/v.swf
#""")
