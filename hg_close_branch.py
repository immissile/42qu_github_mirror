#!/usr/bin/env python
#coding:utf-8


branches = """
yup_20111219_google_login   8337:796ef5072483
wooparadog_20111219_syntaxhigh 8341:b6051bc98da2 (inactive)
zuroc_20111231_newbie       8338:0dbc20858d46 (inactive)
zuroc_20111218_book         8284:aa9ce0b0e18f (inactive)
"""

branches = branches.strip()

for i in branches.split('\n'):
    j = i.split(' ', 1)[0]
    print 'hg update %s ; hg commit --close-branch -m close;'%j

print 'hg update default'

