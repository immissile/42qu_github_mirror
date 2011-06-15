#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, abspath, dirname


import sys

from creole import Parser
from creole.html_emitter import HtmlEmitter

def wiki2html(wiki):
    document = Parser(wiki).parse()
    return HtmlEmitter(document).emit().encode('utf-8', 'ignore')

HTML_TEMPLATE = """
<!doctype html>
<head><meta http-equiv="content-type" content="text/html; charset=UTF-8">
<style>
a{text-decoration:none;color:#01c}
a:hover{text-decoration:none;color:#a10}

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 16px;
    font: inherit;
    vertical-align: baseline;
    font-family:Georgia;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, section {
    display: block;
}
body {
    line-height: 1;
}
.content{
font-size:16px;
padding:14px 0;
width:700px;
margin:auto;
line-height:32px;
font-family:Georgia;
}
h1{
text-align:center;
border:1px dotted #ccc;
margin:14px 0;
padding:14px 0;
}
h2{
margin:48px 0 16px;
padding:8px 0;
border-bottom:1px dotted #ccc;
border-top:1px dotted #ccc;
text-align:center;
}
h3{
margin:7px 0;
line-height:18px;
padding-left:8px;
border-left:4px solid #ccc;
}
pre{
font-family:Consolas,Verdana;
padding:14px;
border:1px dotted #ccc;
background:#fefefe;
word-wrap:break-word;overflow:hidden;word-break:break-all;white-space:pre-wrap;white-space:-moz-pre-wrap;*white-space:pre;*word-wrap:break-word;
margin-bottom:14px;
}
</style>
</head>
<body>
<div style="border-bottom:1px dotted #ccc;padding:22px 0 27px;margin-bottom:14px;text-align:center"><a style="font-size:23px;font-family:Trebuchet MS;color:#a10" href="/">42qu.com</a></div>
<div class="content">%s</div>
<div style="border-top:1px dotted #ccc;padding:27px;margin-top:27px;text-align:center"><a href="/" style="font-size:23px;font-family:Trebuchet MS;margin-top:27px;color:#666;padding:14px 28px">42qu.com</a> </div>
<div style="margin:32px 0 64px;text-align:center;">
<a href="http://42qu.com/zuroc" target="_blank">Powered by 张沈鹏 !</a>
</div>
</body>
"""

BASE = dirname(abspath(__file__))

for base, dirs, files in os.walk(BASE):
    for file in files:
        if not file.endswith(".wiki"):
            continue
        wiki = join(base, file)
        if file == "Home.wiki" :
            html_name = "index.html"
        else:
            html_name = wiki[:-5]+".html"

        with open(wiki) as file:
            html = wiki2html(file.read().decode('utf-8', 'ignore'))
            with open(html_name, "w") as out:
                out.write(HTML_TEMPLATE%html)
