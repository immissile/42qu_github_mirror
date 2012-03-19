#coding:utf-8
IMPORT_IGNORE = set(filter(bool,map(str.strip,"""
config
config.dev
_db
_url
_env
""".strip().split("\n"))))

FILE_IGNORE = set(filter(bool,map(str.strip,"""
_handler
server_mq
__init__
_url
_istarsea
_zpage
_db
shortcut
""".strip().split("\n"))))

from os.path import basename

def import_ignore(filename, name):
    if basename(filename)[:-3] in FILE_IGNORE:
        return True
    name = name.replace("import ",'').strip()
    name = name.replace("from ",'').split(" ",1)[0]
    if name in IMPORT_IGNORE:
        return True

    
