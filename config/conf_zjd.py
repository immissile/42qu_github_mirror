#!/usr/bin/env python
# -*- coding: utf-8 -*-
import conf

def main():
    conf.SITE_DOMAIN = 'zjd.me'
    conf.PIC_URL = 'http://p.zjd.me'
    conf.FS_URL = 'http://s.zjd.me'
    conf.PORT = 6666
    conf.MYSQL_MAIN = 'zpage'
    print "\!!!",conf.SITE_DOMAIN
