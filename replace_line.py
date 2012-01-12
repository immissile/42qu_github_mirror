#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import abspath, dirname, basename, join
from os import walk

FROM_STRING = """
    upyun_path_builder 
    upyun_username 
    upyun_pwd 
    upyun_spacename 
    upyun_api_url 
    upyun_domain 
    upyun_dirname 
"""

TO_STRING = """
    UPYUN_PATH_BUILDER 
    UPYUN_USERNAME 
    UPYUN_PWD 
    UPYUN_SPACENAME 
    UPYUN_API_URL 
    UPYUN_DOMAIN 
    UPYUN_DIRNAME 
"""

def run():
    from_string = FROM_STRING.strip()
    to_string = TO_STRING.strip()
    for from_s, to_s in zip(FROM_STRING.split('\n'), TO_STRING.split('\n')):
        replace(from_s.strip(), to_s.strip())

def replace(from_string, to_string):
    from_string = from_string.strip()
    to_string = to_string.strip()

    file = abspath(__file__)

    for dirpath, dirnames, filenames in walk(dirname(file)):
        dirbase = basename(dirpath)
        if dirbase.startswith('.'):
            continue

        for filename in filenames:
            suffix = filename.rsplit('.', 1)[-1]
            if suffix not in ('py', 'htm', 'txt', 'conf', 'css', 'h', 'template', 'js'):
                continue
            path = join(dirpath, filename)
            if path == file:
                continue
            with open(path) as f:
                content = f.read()
            t = content.replace(from_string, to_string)
            if t != content:
                with open(path, 'wb') as f:
                    f.write(t)

run()
