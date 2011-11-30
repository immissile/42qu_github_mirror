#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from os.path import join, abspath, dirname

import sys

sys.path.append( dirname(dirname(dirname(dirname(abspath(__file__))))) )

from static import js

from zkit.creole import Parser
from zkit.creole.html_emitter import HtmlEmitter

def wiki2html(wiki):
    document = Parser(wiki).parse()
    return HtmlEmitter(document).emit().encode('utf-8', 'ignore')

HTML_TEMPLATE = ''.join(['''
<!doctype html>
<head><meta http-equiv="content-type" content="text/html; charset=UTF-8">
<script src="''',
'http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.6.1.min.js',
'''"></script>
<script src="/help.js"></script>
<script src="http://hm.baidu.com/h.js?1248415989221c81fd45dd0d1208df98"></script>
<link href="/help.css" rel="stylesheet" type="text/css">
</head>
<body>
<div style="border-bottom:1px dotted #ccc;padding:22px 0 27px;margin-bottom:14px;text-align:center">
<a style="font-size:23px;font-family:Trebuchet MS;color:#d10" href="/">42qu.com</a></div>
<div class="content">%s</div>
<div style="border-top:1px dotted #ccc;padding:27px;margin-top:27px;text-align:center">
<a href="/" style="font-size:23px;font-family:Trebuchet MS;margin-top:27px;color:#666;padding:14px 28px">42qu.com</a>
</div>
</body>
'''])

BASE = dirname(abspath(__file__))

for base, dirs, files in os.walk(BASE):
    for file in files:
        if not file.endswith('.wiki'):
            continue
        wiki = join(base, file)
        if file == 'Home.wiki':
            html_name = 'index.html'
        else:
            html_name = wiki[:-5] + '.html'

        with open(wiki) as file:
            html = wiki2html(file.read().decode('utf-8', 'ignore'))
            with open(html_name, 'w') as out:
                out.write(HTML_TEMPLATE%html)




