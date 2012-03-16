#coding:utf-8
import re
from xml.sax.saxutils import unescape

def txttidy_feed43(txt):
    return txt.replace('<p><sub><i>-- Delivered by <a href="http://feed43.com/">Feed43</a> service</i></sub></p>', '')


#RE_42QU = re.compile(r''' style="([^\"]*)">(.*)$''')

def txttidy_42qu(txt):
    first_pos = txt.find('<div id="qu42"')
    if first_pos <= 0:
        tmp = txt.find('关于作者')
        if tmp >= 0:
            txt = txt[:tmp]
        first_pos = txt.rfind('<div style="border:1px')
        if first_pos <= 0:
            return txt
    txt = txt[:first_pos]
    return txt

def txttidy_wumii(txt):
    pos = txt.find('http://app.wumii.com')
    if pos > 0:
        txt = txt[:pos]
        txt = txt[:txt.rfind('<table')]

        tmp = txt.find('猜您也喜欢')
        if tmp < 0:
            tmp = txt.find('相关文章')
        if tmp >= 0:
            return txt[:tmp]

    return txt

def txttidy_other_relate(txt):
    pos = txt.find('>相关阅读推荐')
    if pos > 0:
        txt = txt[:pos]
        txt = txt[:txt.rfind('<h3')]
    return txt

def txttidy_bshare(txt):
    first_pos = txt.find('<p><a href="http://sharethis')
    if first_pos >= 0:
        txt = txt[:first_pos]
    return txt

def txttidy_alibuybuy(txt):
    pos = txt.find('<p><small>© 推荐')
    if pos > 0:
        txt = txt[:pos]
    return txt

def txttidy_swf(txt):
    pos_str = 'http://reader.googleusercontent.com/reader/embediframe?src='
    iframe_end = '</iframe>'
    while True:
        bpos = txt.find(pos_str)
        if bpos > 0:
            p2 = bpos+len(pos_str)
            p3 = txt.find('&', p2)
            epos = txt.find(iframe_end, p3)
            txt1 = txt[:bpos]
            txt1 = txt1[:txt1.rfind('<iframe ')]
            txt2 = txt[p2:p3]
            txt3 = txt[epos+len(iframe_end):]
            r = [txt1.rstrip(), txt2, txt3.lstrip()]
            txt = '\n\n'.join(r)
        else:
            break
    return txt

def txttidy_36kr(txt):
    for key in (
'无觅猜您也喜欢',
'您可能也喜欢',
'可能与本文相关的其它文章',
'<p>除非注明，本站文章均为原创或编译，转载请注明： 文章来自',
'与本日志可能相关的文章有',
"随机文章",
    ):
        pos = txt.find(key)
        if pos > 0:
            txt = txt[:pos]

    return txt

def txttidy(txt):
    txt = unescape(txt).replace('&quot;', '"')
    txt = txttidy_36kr(txt)
    txt = txttidy_alibuybuy(txt)
    txt = txttidy_other_relate(txt)
    txt = txttidy_feed43(txt)
    txt = txttidy_42qu(txt)
    txt = txttidy_wumii(txt)
    txt = txttidy_bshare(txt)
    txt = txttidy_swf(txt)
    txt = txt.rstrip().rstrip("\n").rstrip("*")
    return txt


if __name__ == '__main__':
    txt = """Google Reader 视频<iframe src="http://reader.googleusercontent.com/reader/embediframe?src=http://player.youku.com/player.php/sid/XMjQ2ODM1Mjcy/v.swf&;amp;width=600&amp;height=500" width="600" height="500"></iframe>加勒比海盗"""
    def grab_str(string):
        print re.sub('<iframe.*(embediframe\?src\=)(.*\.swf).*', '\\2', string)
    grab_str(txt)
    from glob import glob

    for f in reversed(sorted(glob('test/*.txt'))):
        with open(f) as infile:
            print txttidy(infile.read())
            raw_input(f)

