#!/usr/bin/env python
# -*- coding: utf-8 -*-

def img_filter(url):
    if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.swf') or url.endswith('.gif'):
        return True
    return False


